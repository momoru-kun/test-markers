import json
from json.encoder import JSONEncoder
from django.http.response import JsonResponse
from django.views.generic import View
from .utils import get_client_ip, clean_comment_from_garbage
from .models import Comment
from markers.models import Picture
from datetime import datetime


class CommentView(View):
    PER_PAGE = 10

    def get(self, request, *args, **kwargs):
        picture_id = request.GET.get('id')
        page = request.GET.get('page')

        if picture_id is None:
            return JsonResponse({
                "status": "error",
                "description": "id field is required"
            }, status=400)

        picture = Picture.objects.get(id = picture_id)
        comments = [comment.to_dict() for comment in picture.comment_set.all()]

        return JsonResponse({'result': comments})

    def post(self, request, *args, **kwargs):
        post = json.loads(request.body)
        picture_id = post.get('id')
        email = post.get('email')
        text = post.get('text')

        if email is None or text is None:
            error = "{}{}".format(
                'email is required;' if email is None else '',
                'text is required' if text is None else ''
            )
            return JsonResponse({
                'status': 'error', 
                'description': error
            }, status=400)

        if len(clean_comment_from_garbage(text)) == 0:
            return JsonResponse({"status": "error", "description": "empty text (maybe only <script> xD)"}, status=400)

        Picture.objects.get(id = picture_id).comment_set.create(
            email = email, 
            ip_addr = get_client_ip(request),
            text = clean_comment_from_garbage(text),
            send_date = datetime.now()
        )

        return JsonResponse({'status': 'ok'})
        
