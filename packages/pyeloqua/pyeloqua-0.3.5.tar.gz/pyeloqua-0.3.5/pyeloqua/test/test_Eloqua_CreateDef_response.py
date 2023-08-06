export_activity = {
    "name":"test",
    "fields":{
        "ActivityId":"{{Activity.Id}}"
    },
    "filter":"'{{Activity.Type}}'='EmailSend'",
    "dataRetentionDuration":"P7D",
    "uri":"/activities/exports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}

export_contacts = {
    "name": "test",
    "fields": {
        "EmailAddress": "{{Contact.Field(C_EmailAddress)}}"
    },
    "dataRetentionDuration": "P7D",
    "uri": "/contacts/exports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}

export_accounts = {
    "name":"test",
    "fields":{
        "AccountName":"{{Account.Field(M_CompanyName)}}"
    },
    "dataRetentionDuration":"P7D",
    "uri":"/accounts/exports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}

export_customobjects = {
    "name":"test",
    "fields":{
        "ID":"{{CustomObject[1].ExternalId}}"
    },
    "dataRetentionDuration":"P7D",
    "uri":"/customObjects/1/exports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}


import_contacts = {
    "name": "test",
    "fields": {
        "EmailAddress": "{{Contact.Field(C_EmailAddress)}}"
    },
    "dataRetentionDuration": "P7D",
    "uri": "/contacts/imports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}

import_accounts = {
    "name":"test",
    "fields":{
        "AccountName":"{{Account.Field(M_CompanyName)}}"
    },
    "dataRetentionDuration":"P7D",
    "uri":"/accounts/imports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}

import_customobjects = {
    "name":"test",
    "fields":{
        "ID":"{{CustomObject[1].ExternalId}}"
    },
    "dataRetentionDuration":"P7D",
    "uri":"/customObjects/1/imports/1234",
    "createdBy":"Test.User",
    "createdAt":"2015-01-01T11:09:00.0000004Z",
    "updatedBy":"Test.User",
    "updatedAt":"2015-01-01T11:09:00.0000004Z"
}


bad_import = {
  "failures": [
    {
      "field": "BadField",
      "stackTrace": [
        {
          "field": "fields"
        }
      ],
      "value": "{{Contact.Field(C_BadField)}}",
      "constraint": "Must be a reference to an existing object."
    }
  ]
}
