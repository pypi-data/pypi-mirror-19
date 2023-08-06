
import requests
import json

webhook_url = 'https://hooks.slack.com/services/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'



def get_ticket():
    JSON_Response = {
        "id":               2545,
        "url":              "https://prismskylabs.zendesk.com/agent/tickets/2540",
        "external_id":      "Villa",
        "created_at":       "2009-07-20T22:55:29Z",
        "updated_at":       "2011-05-05T10:38:52Z",
        "type":             "incident",
        "subject":          "Test - Counting Data not showing up in the application",
        "raw_subject":      "{{dc.Test - Counting Data is not showing up in the application}}",
        "description":      "Counting data is not showing up in the application",
        "priority":         "high",
        "status":           "open",
        "recipient":        "support@prism.com",
        "requester_id":     20978392,
        "submitter_id":     76872,
        "assignee_id":      235323,
        "organization_id":  509974,
        "group_id":         98738,
        "collaborator_ids": [35334, 234],
        "forum_topic_id":   72648221,
        "problem_id":       9873764,
        "has_incidents":    'false',
        "due_at":           'null',
        "tags":             ["other_tag"],
        "via": {
            "channel": "web"
        },
        "custom_fields": [
            {
            "id":    27642,
            "value": "745"
            },
            {
            "id":    27648,
            "value": "yes"
            }
        ],
    }
    return JSON_Response



def ticket_parameters():
    #r = requests.get('https://github.com/timeline.json')
    ticket = get_ticket()
    ticket_id = ticket['id']
    ticket_title = ticket['subject']
    ticket_text = ticket['description']
    ticket_url = ticket['url']
    ticket_account = ticket['external_id']
    
    slack_ticket = { "text": "New Ticket from %s: Ticket #%s" % (ticket_account, ticket_id),
                     "attachments": [
                     {
                        "Text": "Zendesk \n\n",
                        "color": "#36a64f",
                        "author_name": "Zendesk",
                        "author_link": "https://prismskylabs.zendesk.com/agent/dashboard",
                        "author_icon": "https://c1.staticflickr.com/3/2755/4323030680_ab5c9a70d1.jpg",
                        "title": "%s" % ticket_title,
                        "title_link": "%s" % ticket_url,
                        "text": "%s" % ticket_text,
                        "attachment_type": "default",
                            "actions": [
                            {
                                "name": "Reply-Button",
                                "text": "Reply",
                                "type": "button",
                                "value": "reply",
                                "style": "default"
                            },
                            {
                                "name": "Forward-Button",
                                "text": "Forward",
                                "type": "button",
                                "value": "forward"
                            },
                            {
                                "name": "Assign",
                                "text": "Assign",
                                "type": "button",
                                "value": "assign"
                            },
                            {
                                "name": "Close-Button",
                                "text": "Close Ticket",
                                "type": "button",
                                "value": "close",
                                "confirm": {
                                    "title": "Are you sure?",
                                    "text": "Are you sure you want to close this ticket?",
                                    "ok_text": "Yes",
                                    "dismiss_text": "No"
                                    }
                            }
                        ]
                    }
                ]
            }
    
    return slack_ticket



def main():
    payload = ticket_parameters()
    r = requests.post(webhook_url, data=json.dumps(payload))

if __name__ == '__main__':
    main()