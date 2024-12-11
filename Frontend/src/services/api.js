import axios from 'axios'
import { ApiURL } from '../utils/configurations/apiUrl'

export const validateInitialFile = (files,closing_date,fund_type,over_write) => {
    const formData = new FormData();
    files.forEach((file) => {
        formData.append('file', file);
        
    });
    formData.append('closing_date',closing_date)
    formData.append('fund_type',fund_type)
    formData.append('over_write',over_write)

    const response =  axios.post(`${ApiURL}/dashboard/upload_fund_file`, formData, {
            withCredentials:true,
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response;
}
export const getDateReport = async (closing_date) => {
    // const formData = new FormData();
    // formData.append("closing_date", closing_date);
    // formData.append("user_id", 1);
  const dataDate ={     
    closing_date:closing_date,
    user_id:1
  } 
    const response = await axios.post(`${ApiURL}/dashboard/get_bb_data_of_date`,dataDate, {
      withCredentials: true,
    });
  
    return response; 
  };

export const uploadInitialFile = (file_data) => {

    // try {   
        const response = axios.post(`${ApiURL}/dashboard/calculate_bb`, file_data, {
            withCredentials:true,
            
        });
        return response;
};

export const EbitdaAnalysis = (base_data_file_id, type, asset_percent_list) => {
    const payload = {
        "base_data_file_id": base_data_file_id,
        "type": type,
        "asset_percent_list":asset_percent_list
    }
    
        const response = axios.post(`${ApiURL}/wia/update_parameters`, payload, {
            withCredentials:true,
        });
        return response;
    
}

// export const SaveAnalysis =(EbitdaValue,base_file,to_save)=>{
//     const formData = new FormData();
//         formData.append('Financials LTM EBITDA ($MMs)', EbitdaValue);
//         formData.append('user_id',1)
//         formData.append('to_save',to_save)
//         formData.append('base data file name',base_file)
    
//         const response = axios.post(`${ApiURL}/changeEBITDA`, formData, {
//             withCredentials:true,
//         });
        
//         return response;
// }

export const OverviewTableData = (value,fileId,user_id) => {

    const apiData =  {
        'card_name' : value,
        'base_data_file_id' : fileId,
        'user_id':user_id,
    }
    const response = axios.post(`${ApiURL}/dashboard/get_card_overview_data`,apiData , {
        withCredentials:true,
    });
    return response;
}

export const get_preview_table =(selectedFiles) =>{
    const formData = new FormData();
    selectedFiles.forEach((selectedFile) => {
        formData.append('file', selectedFile);
        
    });
    const res =   axios.post(`${ApiURL}/wia/get_asset_overview`,formData,{
        withCredentials:true
    });
        return res
}


export const addNewAsset = async (files,base_file,to_save,selected_Assets_data,inputValueUntitled,descriptionInput,whatIfAnalysisType,whatIfAnalysisId) => {
   
    const payload = {
        base_data_file_id: base_file,
        to_save: to_save,
        simulation_name: inputValueUntitled,
        note: descriptionInput,
        selected_assets:selected_Assets_data,
        what_if_analysis_type:whatIfAnalysisType,
        temporary_what_if_analysis_id:whatIfAnalysisId


    }

    try {   
        const response = await axios.post(`${ApiURL}/wia/add_asset`, payload, {
            // withCredentials:true,
            // headers: {
            //     'Content-Type': 'multipart/form-data',
            // },
        });
        return response;
    } catch (error) {
        console.error('Error uploading file:', error);
        throw error;
    }
};

export const uploadedFileList = () =>{
    const res =   axios.post(`${ApiURL}/dashboard/get_files_list`, {user_id:'1'});
        return res
}



export const getListOfWhatIfAnalysis = (user_id) =>{
    const res = axios.post(`${ApiURL}/wia/wia_library`, {user_id:user_id});
    return res
}

export const getSelectedWIAAsstes = (whatIfAnalysisId,whatIfAnalysisType) =>{
    
    const res = axios.post(`${ApiURL}/get_selected_WIA_asstes`, {
        what_if_analysis_id:whatIfAnalysisId,
        what_if_analysis_type:whatIfAnalysisType
    });
    return res
}

export const getWhatIfAnalysisData = (what_if_analysis_id) => {
    const res = axios.post(`${ApiURL}/select_what_if_analysis`, {what_if_analysis_id:what_if_analysis_id});
    return res
    
}


export const lineChartData = (user_id,fund_type) => 
{
    const formData = new FormData();
    formData.append("user_id",user_id)
    formData.append("fund_type",fund_type)
    const res = axios.post(`${ApiURL}/dashboard/trend_graph`, formData)
    return res

}

export const downloadExcelAssest =(previewData) =>{
    const res = axios.post(`${ApiURL}/download_excel_for_assets`, {assets_to_download:previewData},{
        responseType:'blob',
        headers:{
            "Content-Type":'application/json'
        }
    });
    return res;
}
export const downLoadReportSheet = (base_data_file_id, user_id) => 
{
    const reportSheetData= {
        base_data_file_id:base_data_file_id,
        user_id:user_id
    }

    const res = axios.post(`${ApiURL}/download_excel`, reportSheetData,{
        responseType:'blob',
        headers:{
            "Content-Type":'application/json'
        }
    })
    return res

}

export const landingPageData = (user_id) => {

    const payload = new FormData();
    payload.append('user_id' , user_id);

    const res = axios.post(`${ApiURL}/dashboard/latest_closing_date`, payload)
    return res;
}

export const assetSelectionList = (base_file_id) => {
    const payload = {
        base_data_file_id : base_file_id
    }

    const res = axios.post(`${ApiURL}/dashboard/get_assets_list`,payload,{
        withCredentials:true
    });
    return res;

}

export const intermediateMetricsTable =(base_data_file_id,whatIfAnalysisId) =>{
    const response = axios.post(`${ApiURL}/get_intermediate_metrics`, {
        "base_data_file_id": base_data_file_id,
        "what_if_id":whatIfAnalysisId
    }, {
        withCredentials:true,
    });
    return response;
}

export const setConfigurations = (payload) => {
    const response = axios.post(`${ApiURL}/set_user_config` , payload);
    return response;
}

export const preveiousParamerts  = (user_id) => {
    const res = axios.post(`${ApiURL}/get_selected_columns`, {
        user_id : user_id,
    })
    return res;
} 

export const previousAssets  = (base_file_id) => {
    const res = axios.post(`${ApiURL}/get_previous_assets`, {
        base_data_file_id : base_file_id,
    })
    return res;
} 

export const changeParameter = (base_file_id,parameter) =>{
    const res = axios.post(`${ApiURL}/wia/get_parameters`, {
        base_data_file_id : base_file_id,
        type:parameter
    })
    return res;
}

export const drillDownData = (user_id, base_data_file_id, col_name, row_name,whatIfAnalysisId) => {
    const payload ={   
        "user_id" : user_id,
        "base_data_file_id":base_data_file_id ,
        "col_name" : col_name,
        "row_name" : row_name,
        "what_if_id":whatIfAnalysisId
    }

    const res = axios.post(`${ApiURL}/get_mathematical_formula`, payload);
    return res;
}

export const getConentrationData = (user_id, base_file_id,prev_hairCut) => {
    const payload ={   
        "user_id" : user_id,
        "base_data_file_id":base_file_id ,
        "previous_haircut_column":prev_hairCut
    }

    const res = axios.post(`${ApiURL}/get_concentration_data`, payload);
    return res;
}

export const getConenctrationAnalysis = (base_data_file_id, updated_columns, prev_actual, prev_result) => {
    const payload ={   
        "base_data_file_id" : base_data_file_id,
        "updated_column_list":updated_columns ,
        "previous_actual_column":prev_actual,
        "previous_result_column":prev_result,
    }

    const res = axios.post(`${ApiURL}/concentration_data_analysis`, payload);
    return res;
}

export const lockHairCutTestData = (base_data_file_id, asset_haircut_number_map) => {
    const hairCutTestData = {
        "base_data_file_id":base_data_file_id,
        "asset_haircut_number_mapping":asset_haircut_number_map,
        "over_write":1
    }

    const res = axios.post(`${ApiURL}/lock_concentration_test`, hairCutTestData)
    return res;
}

export const getUpdateAssetData = (base_data_file_id, sheetName,whatIfAnalysisId) => {
    const updateAssetData = {
        "base_data_file_id": base_data_file_id,
        "sheet_name":sheetName,
        "what_if_analysis_id":whatIfAnalysisId
    }

    const res = axios.post(`${ApiURL}/wia/get_base_data_file_sheet_data` , updateAssetData)
    return res;
}

export const updateSheetValues = (base_data_file_id,sheet_name, assetsChanges,what_if_analysis_id) => {
    const updatedSheetData = {
        base_data_file_id:base_data_file_id,
        what_if_analysis_id:what_if_analysis_id,
        sheet_name:sheet_name,
        changes:assetsChanges
    }
    const res = axios.post(`${ApiURL}/wia/update_values_in_sheet`, updatedSheetData);
    return res;
}

export const updateModifiedAssets = (what_if_analysis_id) => {
    const payload = {
        modified_base_data_file_id :what_if_analysis_id,
    }
    const res = axios.post(`${ApiURL}/calculate_bb_modified_sheets` , payload)
    return res

}

export const saveWhatIfAnalysis =(whatIfAnalysisType,whatIfAnalysisId,whatifAnalysisName,whatifAnalysisNote)=>{
    const payload = {
        what_if_analysis_id :whatIfAnalysisId,
        analysis_type: whatIfAnalysisType,
        simulation_name:whatifAnalysisName,
        note:whatifAnalysisNote,
    }
    const res = axios.post(`${ApiURL}/wia/save_analysis` , payload)
    return res
}

export const getConcentrationTestMasterData =(fund_name)=>{
    const payload = {
        fund_name:fund_name
    }
    const res = axios.post(`${ApiURL}/fund_setup/get_concentration_tests` , payload)
    return res
}

export const changeConcentrationTestMasterData =(changes)=>{
    const payload = {
        changes:changes
    }
    const res = axios.post(`${ApiURL}/fund_setup/change_limit_percent` , payload)
    return res
}