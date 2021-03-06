from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View
from .models import Picture

class PictureView(View):

    def get(self, request, *args, **kwargs):
        last_picture_id = request.session.get('last_picture')
        new_picture = request.GET.get('id')

        picture = None
        
        if not (new_picture is None):
            # If client request picture by marker
            picture = get_object_or_404(Picture, id = new_picture)

        elif (last_picture_id is None) and (new_picture is None):
            # If new user without session_id
            picture = Picture.objects.first()
        
        else:
            # If old user - restore last picture ID from session storage
            picture = Picture.objects.get(id = last_picture_id)

        request.session['last_picture'] = picture.id
        return JsonResponse(picture.to_dict())
