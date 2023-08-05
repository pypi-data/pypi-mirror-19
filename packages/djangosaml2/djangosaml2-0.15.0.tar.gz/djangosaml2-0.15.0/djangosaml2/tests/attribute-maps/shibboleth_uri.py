EDUPERSON_OID = "urn:oid:1.3.6.1.4.1.5923.1.1.1."
X500ATTR = "urn:oid:2.5.4."
NOREDUPERSON_OID = "urn:oid:1.3.6.1.4.1.2428.90.1."
NETSCAPE_LDAP = "urn:oid:2.16.840.1.113730.3.1."
UCL_DIR_PILOT = "urn:oid:0.9.2342.19200300.100.1."
PKCS_9 = "urn:oid:1.2.840.113549.1.9."
UMICH = "urn:oid:1.3.6.1.4.1.250.1.57."

MAP = {
    "identifier": "urn:mace:shibboleth:1.0:attributeNamespace:uri",
    "fro": {
        EDUPERSON_OID+'2': 'eduPersonNickname',
        EDUPERSON_OID+'9': 'eduPersonScopedAffiliation',
        EDUPERSON_OID+'11': 'eduPersonAssurance',
        EDUPERSON_OID+'10': 'eduPersonTargetedID',
        EDUPERSON_OID+'4': 'eduPersonOrgUnitDN',
        NOREDUPERSON_OID+'6': 'norEduOrgAcronym',
        NOREDUPERSON_OID+'7': 'norEduOrgUniqueIdentifier',
        NOREDUPERSON_OID+'4': 'norEduPersonLIN',
        EDUPERSON_OID+'1': 'eduPersonAffiliation',
        NOREDUPERSON_OID+'2': 'norEduOrgUnitUniqueNumber',
        NETSCAPE_LDAP+'40': 'userSMIMECertificate',
        NOREDUPERSON_OID+'1': 'norEduOrgUniqueNumber',
        NETSCAPE_LDAP+'241': 'displayName',
        UCL_DIR_PILOT+'37': 'associatedDomain',
        EDUPERSON_OID+'6': 'eduPersonPrincipalName',
        NOREDUPERSON_OID+'8': 'norEduOrgUnitUniqueIdentifier',
        NOREDUPERSON_OID+'9': 'federationFeideSchemaVersion',
        X500ATTR+'53': 'deltaRevocationList',
        X500ATTR+'52': 'supportedAlgorithms',
        X500ATTR+'51': 'houseIdentifier',
        X500ATTR+'50': 'uniqueMember',
        X500ATTR+'19': 'physicalDeliveryOfficeName',
        X500ATTR+'18': 'postOfficeBox',
        X500ATTR+'17': 'postalCode',
        X500ATTR+'16': 'postalAddress',
        X500ATTR+'15': 'businessCategory',
        X500ATTR+'14': 'searchGuide',
        EDUPERSON_OID+'5': 'eduPersonPrimaryAffiliation',
        X500ATTR+'12': 'title',
        X500ATTR+'11': 'ou',
        X500ATTR+'10': 'o',
        X500ATTR+'37': 'cACertificate',
        X500ATTR+'36': 'userCertificate',
        X500ATTR+'31': 'member',
        X500ATTR+'30': 'supportedApplicationContext',
        X500ATTR+'33': 'roleOccupant',
        X500ATTR+'32': 'owner',
        NETSCAPE_LDAP+'1': 'carLicense',
        PKCS_9+'1': 'email',
        NETSCAPE_LDAP+'3': 'employeeNumber',
        NETSCAPE_LDAP+'2': 'departmentNumber',
        X500ATTR+'39': 'certificateRevocationList',
        X500ATTR+'38': 'authorityRevocationList',
        NETSCAPE_LDAP+'216': 'userPKCS12',
        EDUPERSON_OID+'8': 'eduPersonPrimaryOrgUnitDN',
        X500ATTR+'9': 'street',
        X500ATTR+'8': 'st',
        NETSCAPE_LDAP+'39': 'preferredLanguage',
        EDUPERSON_OID+'7': 'eduPersonEntitlement',
        X500ATTR+'2': 'knowledgeInformation',
        X500ATTR+'7': 'l',
        X500ATTR+'6': 'c',
        X500ATTR+'5': 'serialNumber',
        X500ATTR+'4': 'sn',
        UCL_DIR_PILOT+'60': 'jpegPhoto',
        X500ATTR+'65': 'pseudonym',
        NOREDUPERSON_OID+'5': 'norEduPersonNIN',
        UCL_DIR_PILOT+'3': 'mail',
        UCL_DIR_PILOT+'25': 'dc',
        X500ATTR+'40': 'crossCertificatePair',
        X500ATTR+'42': 'givenName',
        X500ATTR+'43': 'initials',
        X500ATTR+'44': 'generationQualifier',
        X500ATTR+'45': 'x500UniqueIdentifier',
        X500ATTR+'46': 'dnQualifier',
        X500ATTR+'47': 'enhancedSearchGuide',
        X500ATTR+'48': 'protocolInformation',
        X500ATTR+'54': 'dmdName',
        NETSCAPE_LDAP+'4': 'employeeType',
        X500ATTR+'22': 'teletexTerminalIdentifier',
        X500ATTR+'23': 'facsimileTelephoneNumber',
        X500ATTR+'20': 'telephoneNumber',
        X500ATTR+'21': 'telexNumber',
        X500ATTR+'26': 'registeredAddress',
        X500ATTR+'27': 'destinationIndicator',
        X500ATTR+'24': 'x121Address',
        X500ATTR+'25': 'internationaliSDNNumber',
        X500ATTR+'28': 'preferredDeliveryMethod',
        X500ATTR+'29': 'presentationAddress',
        EDUPERSON_OID+'3': 'eduPersonOrgDN',
        NOREDUPERSON_OID+'3': 'norEduPersonBirthDate',
    },
    "to":{
        'roleOccupant': X500ATTR+'33',
        'gn': X500ATTR+'42',
        'norEduPersonNIN': NOREDUPERSON_OID+'5',
        'title': X500ATTR+'12',
        'facsimileTelephoneNumber': X500ATTR+'23',
        'mail': UCL_DIR_PILOT+'3',
        'postOfficeBox': X500ATTR+'18',
        'fax': X500ATTR+'23',
        'telephoneNumber': X500ATTR+'20',
        'norEduPersonBirthDate': NOREDUPERSON_OID+'3',
        'rfc822Mailbox': UCL_DIR_PILOT+'3',
        'dc': UCL_DIR_PILOT+'25',
        'countryName': X500ATTR+'6',
        'emailAddress': PKCS_9+'1',
        'employeeNumber': NETSCAPE_LDAP+'3',
        'organizationName': X500ATTR+'10',
        'eduPersonAssurance': EDUPERSON_OID+'11',
        'norEduOrgAcronym': NOREDUPERSON_OID+'6',
        'registeredAddress': X500ATTR+'26',
        'physicalDeliveryOfficeName': X500ATTR+'19',
        'associatedDomain': UCL_DIR_PILOT+'37',
        'l': X500ATTR+'7',
        'stateOrProvinceName': X500ATTR+'8',
        'federationFeideSchemaVersion': NOREDUPERSON_OID+'9',
        'pkcs9email': PKCS_9+'1',
        'givenName': X500ATTR+'42',
        'x500UniqueIdentifier': X500ATTR+'45',
        'eduPersonNickname': EDUPERSON_OID+'2',
        'houseIdentifier': X500ATTR+'51',
        'street': X500ATTR+'9',
        'supportedAlgorithms': X500ATTR+'52',
        'preferredLanguage': NETSCAPE_LDAP+'39',
        'postalAddress': X500ATTR+'16',
        'email': PKCS_9+'1',
        'norEduOrgUnitUniqueIdentifier': NOREDUPERSON_OID+'8',
        'eduPersonPrimaryOrgUnitDN': EDUPERSON_OID+'8',
        'c': X500ATTR+'6',
        'teletexTerminalIdentifier': X500ATTR+'22',
        'o': X500ATTR+'10',
        'cACertificate': X500ATTR+'37',
        'telexNumber': X500ATTR+'21',
        'ou': X500ATTR+'11',
        'initials': X500ATTR+'43',
        'eduPersonOrgUnitDN': EDUPERSON_OID+'4',
        'deltaRevocationList': X500ATTR+'53',
        'norEduPersonLIN': NOREDUPERSON_OID+'4',
        'supportedApplicationContext': X500ATTR+'30',
        'eduPersonEntitlement': EDUPERSON_OID+'7',
        'generationQualifier': X500ATTR+'44',
        'eduPersonAffiliation': EDUPERSON_OID+'1',
        'eduPersonPrincipalName': EDUPERSON_OID+'6',
        'localityName': X500ATTR+'7',
        'owner': X500ATTR+'32',
        'norEduOrgUnitUniqueNumber': NOREDUPERSON_OID+'2',
        'searchGuide': X500ATTR+'14',
        'certificateRevocationList': X500ATTR+'39',
        'organizationalUnitName': X500ATTR+'11',
        'userCertificate': X500ATTR+'36',
        'preferredDeliveryMethod': X500ATTR+'28',
        'internationaliSDNNumber': X500ATTR+'25',
        'uniqueMember': X500ATTR+'50',
        'departmentNumber': NETSCAPE_LDAP+'2',
        'enhancedSearchGuide': X500ATTR+'47',
        'userPKCS12': NETSCAPE_LDAP+'216',
        'eduPersonTargetedID': EDUPERSON_OID+'10',
        'norEduOrgUniqueNumber': NOREDUPERSON_OID+'1',
        'x121Address': X500ATTR+'24',
        'destinationIndicator': X500ATTR+'27',
        'eduPersonPrimaryAffiliation': EDUPERSON_OID+'5',
        'surname': X500ATTR+'4',
        'jpegPhoto': UCL_DIR_PILOT+'60',
        'eduPersonScopedAffiliation': EDUPERSON_OID+'9',
        'protocolInformation': X500ATTR+'48',
        'knowledgeInformation': X500ATTR+'2',
        'employeeType': NETSCAPE_LDAP+'4',
        'userSMIMECertificate': NETSCAPE_LDAP+'40',
        'member': X500ATTR+'31',
        'streetAddress': X500ATTR+'9',
        'dmdName': X500ATTR+'54',
        'postalCode': X500ATTR+'17',
        'pseudonym': X500ATTR+'65',
        'dnQualifier': X500ATTR+'46',
        'crossCertificatePair': X500ATTR+'40',
        'eduPersonOrgDN': EDUPERSON_OID+'3',
        'authorityRevocationList': X500ATTR+'38',
        'displayName': NETSCAPE_LDAP+'241',
        'businessCategory': X500ATTR+'15',
        'serialNumber': X500ATTR+'5',
        'norEduOrgUniqueIdentifier': NOREDUPERSON_OID+'7',
        'st': X500ATTR+'8',
        'carLicense': NETSCAPE_LDAP+'1',
        'presentationAddress': X500ATTR+'29',
        'sn': X500ATTR+'4',
        'domainComponent': UCL_DIR_PILOT+'25',
    }
}