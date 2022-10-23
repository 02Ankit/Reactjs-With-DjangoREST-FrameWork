from rest_framework import renderers
import json
# iska use karne se setting me se hata ke custome type bana rahe hai.
class UserRenderer(renderers.JSONRenderer):
    charset='utf-8'

    def render(self,data, accepted_media_type=None, renderer_context = None):
        response = ''
        # agar ErrorDetails hai Data me 'ErrorDetail' in str(data)check (ErrorDetal == ErrorDetail) 
        # view me print karke dekh sakte hai response me error dega hai to wo "ErrorDetail" deta hai exception hatane pe. 
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors':data})
        else:response = json.dumps(data)

        return response