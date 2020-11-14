from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.views.decorators.csrf import csrf_exemptt
from .models import Nodes

@method_decorator(csrf_exempt, name='dispatch')
class NodesView(View):
    def get(self, request, id=None, *args, **kwargs):
        if id is None:
            nodes = list(Nodes.objects.values())
        else:
            nodes = list(Nodes.objects.filter(node_id=id).values())
        return JsonResponse(nodes, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        name = data['name']
        c = Customers(e)
        c.save()
        return HttpResponse(status=200)