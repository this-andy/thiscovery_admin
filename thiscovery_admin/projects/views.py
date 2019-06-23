from django.shortcuts import render
from .aws import get_secret, get_aws_namespace


def index(request):
    # return HttpResponse('Authenticate HubSpot API')
    hubspot_connection = get_secret('hubspot-connection')
    api_key = hubspot_connection['api-key']
    client_id = hubspot_connection['client-id']
    context_dict = {'client_id': client_id, "namespace": get_aws_namespace()}
    return render(request, 'hubspot.html', context=context_dict)