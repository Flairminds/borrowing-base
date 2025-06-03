def company_info_prompt(company_name):
    return '''Give me a detailed corporate profile of ''' + company_name + ''', including the following:
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
		"employee_count": number,
		"products_and_services": Array,
		"key_programs_served": Array,
		"ownership_history": [{
			"date": string in format MM-DD-YYYY,
			"acquirer": string,
			"deal_type": string,
			"details": string
		}],
        "acquisitions_history": [{
			"date": string in format MM-DD-YYYY,
			"acquirer": string,
			"deal_type": string,
			"details": string
		}],
		"parent_company": string,
		"sister_companies": string[],
		"subsidiaries": string[],
		"key_milestones": [{
			"year": number,
			"event": string
		}],
		"partnerships_and_joint_ventures": [{
			"partner": string,
			"type": string,
			"details": string
		}],
		"latest_news_links": string[],
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


# def company_info_prompt(company_name):
#     return '''What is today precise date?'''