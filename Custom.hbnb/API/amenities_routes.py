from flask import request, abort
from flask_restx import Namespace, Resource, fields
from model.amenitycls import Amenity

ns_amenity = Namespace('amenities', description='Amenity operations')

amenity_model = ns_amenity.model('Amenity', {
    'id': fields.String(readOnly=True, description='The unique identifier of an amenity'),
    'name': fields.String(required=True, description='The amenity name'),
    'created_at': fields.DateTime(readOnly=True, description='The date and time the amenity was created'),
    'updated_at': fields.DateTime(readOnly=True, description='The date and time the amenity was last updated')
})

def validate_amenity_data(data):
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        abort(400, description="Amenity name must be a non-empty string")
    all_amenities = Amenity.load_all()
    for amenity in all_amenities:
        if amenity.name == data['name']:
            abort(409, description="Amenity name already exists")

@ns_amenity.route('/')
class AmenityList(Resource):
    @ns_amenity.doc('list_amenities')
    @ns_amenity.marshal_list_with(amenity_model)
    def get(self):
        amenities = Amenity.load_all()
        return amenities

    @ns_amenity.doc('create_amenity')
    @ns_amenity.expect(amenity_model)
    @ns_amenity.marshal_with(amenity_model, code=201)
    def post(self):
        if not request.json:
            abort(400, description="Request payload must be JSON")
        data = request.json
        validate_amenity_data(data)
        amenity = Amenity(name=data['name'])
        return amenity, 201

@ns_amenity.route('/<string:amenity_id>')
@ns_amenity.response(404, 'Amenity not found')
@ns_amenity.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @ns_amenity.doc('get_amenity')
    @ns_amenity.marshal_with(amenity_model)
    def get(self, amenity_id):
        amenity = Amenity.load(amenity_id)
        if not amenity:
            abort(404, description="Amenity not found")
        return amenity

    @ns_amenity.doc('update_amenity')
    @ns_amenity.expect(amenity_model)
    @ns_amenity.marshal_with(amenity_model)
    def put(self, amenity_id):
        amenity = Amenity.load(amenity_id)
        if not amenity:
            abort(404, description="Amenity not found")

        if not request.json:
            abort(400, description="Request payload must be JSON")

        data = request.json
        validate_amenity_data(data)
        amenity.update_details(name=data['name'])
        return amenity

    @ns_amenity.doc('delete_amenity')
    @ns_amenity.response(204, 'Amenity deleted')
    def delete(self, amenity_id):
        amenity = Amenity.load(amenity_id)
        if not amenity:
            abort(404, description="Amenity not found")

        Amenity.delete(amenity_id)
        return '', 204
