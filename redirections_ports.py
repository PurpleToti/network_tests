import upnpy

upnp = upnpy.UPnP()

appareils = upnp.discover()
routeur = upnp.get_igd()
services = routeur.get_services()

service = None

for s in services:
    actions = s.get_actions()

    for action in actions:
        if action.name == "AddPortMapping":
            service = s

def getPublicIp():
    global service

    return service.GetExternalIPAddress()

def getServices():
    global service

    return service.get_actions()

def getParametresOuverturePort():
    global service

    return service.AddPortMapping.get_input_arguments()

def getParametresFermeturePort():
    global service

    return service.DeletePortMapping.get_input_arguments()

def ouvirPort(port_externe, port_interne, adresse_ip, protocole="TCP"):
    global service

    service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=port_externe,
        NewProtocol=protocole,
        NewInternalPort=port_interne,
        NewInternalClient=adresse_ip,
        NewEnabled=1,
        NewPortMappingDescription='Test port mapping entry from UPnPy.',
        NewLeaseDuration=0
    )

def fermerPort(port_externe, adresse_ip, protocole="TCP"):
    global service

    service.DeletePortMapping(
        NewRemoteHost=adresse_ip,
        NewExternalPort=port_externe,
        NewProtocol=protocole
    )

print(getPublicIp())