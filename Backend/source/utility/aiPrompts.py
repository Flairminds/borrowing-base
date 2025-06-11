def company_info_prompt(company_name, google_result):
    return '''Summarize the data provided in the user query to produce a better result.\n''' + google_result + '''\nGive priority to data provided in this prompt in case of conflict. Give me a detailed corporate profile of ''' + company_name + ''', including the following:
    1. Parent company or ownership structure
    2. History of mergers and acquisitions of this company
    3. History of mergers and acquisitions by this company
    4. List of sister companies (companies under the same parent)
    5. List of subsidiaries or child companies
    6. Founding date and historical background
    7. Key milestones in company growth or ownership changes
    8. Relevant partnerships or joint ventures
    Format the output in proper JSON. Cite sources where applicable. Only include verifiable and up-to-date information.
    Give output in following json structure -
    {
		"company_name": string,
		"industry": string,
		"founder": string,
		"current_ceo": string,
		"employee_count": string,
		"products_and_services": Array,
		"key_programs_served": Array,
		"ownership_history": [{
			"date": string in format 'MM-DD-YYYY' or 'Mmm, YYYY',
			"acquirer": string,
			"deal_type": string,
			"details": string
		}],
        "acquisitions_history": [{
			"date": string in format 'MM-DD-YYYY' or 'Mmm, YYYY',
			"acquirer": string,
			"deal_type": string,
			"details": string
		}],
		"parent_company": string,
		"sister_companies": string[],
		"subsidiaries": string[],
		"key_milestones": [{
			"date": string in format 'MM-DD-YYYY' or 'Mmm, YYYY',
			"event": string
		}],
		"partnerships_and_joint_ventures": [{
			"partner": string,
			"type": string,
			"details": string
		}],
		"latest_news_links": [{
			"date": string in format 'MM-DD-YYYY' or 'Mmm, YYYY',
            "link": string
        }],
		"sources": string[]
	}
	If you can't find the result or face any issue, then return that as following json -
	{
		"error": true
		"error_message": string
	}
	If you numerous companies that could potentially match that name return the names of matching companies as following json -
	{
		"error": true
		"suggestions": string[]
	}
    Do not send anything else in output other than json. Use only verifiable sources and do not send wrong results. Check in crunchbase.com for better results.'''
    

def knowledge_graph_prompt(input):
    return input + '''\nGive me the knowledge graph of companies mentioned in this in the following json schema:\n{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "GraphData",
  "type": "object",
  "properties": {
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "label", "type"],
        "properties": {
          "id": { "type": "string" },
          "label": { "type": "string" },
          "type": { "type": "string" },
          "properties": {
            "type": "object",
            "properties": {
              "industry": { "type": "string" },
              "founder": { "type": "string" },
              "current_ceo": { "type": "string" },
              "employee_count": { "type": "integer" },
              "products_and_services": {
                "type": "array",
                "items": { "type": "string" }
              }
            },
            "additionalProperties": true
          }
        },
        "additionalProperties": true
      }
    },
    "edges": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "target", "type"],
        "properties": {
          "source": { "type": "string" },
          "target": { "type": "string" },
          "type": { "type": "string" },
          "properties": {
            "type": "object",
            "properties": {
              "date": { "type": "string" },
              "deal_type": { "type": "string" }
            },
            "additionalProperties": true
          }
        },
        "additionalProperties": true
      }
    }
  },
  "required": ["nodes", "edges"],
  "additionalProperties": false
}
'''
# def company_info_prompt(company_name):
#     return '''What is today precise date?'''