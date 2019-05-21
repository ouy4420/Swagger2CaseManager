import axios from 'axios'
import store from '../store/state'
import router from '../router'
import {Message} from 'element-ui';

// 使用代理后，不需要这两句
// export const baseUrl = "http://192.168.161.1:5000/";
// axios.defaults.baseURL = baseUrl;
axios.defaults.withCredentials = true;
// 现在传的数据都是json，所以content-type值就是application/json
// axios.defaults.headers.post['Content-Type'] = 'application/json;charset=UTF-8';

// pre_request钩子操作
axios.interceptors.request.use(
  function (config) {
    console.log("config", config)
    console.log("config.url", config.url)
    if (config.url.indexOf("/api/waykichain/project/?cursor=\"") !== -1) {

    } else if (!config.url.startsWith("/api/user/")) {
      config.url = config.url.indexOf('?') == '-1' ?
        config.url + "?token=" + store.token + "&user=" + store.user :
        config.url + "&token=" + store.token + "&user=" + store.user;
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

// after_response钩子操作
axios.interceptors.response.use(
  function (response) {
    if (response.data.hasOwnProperty("code")) {
      if (response.data.code === -1) {
        // 切换到Login登录界面
        router.replace({
          name: 'Login'
        });
      }
    } else {
      console.log("token is ok!")
    }

    return response;
  },
  function (error) {
    try {
      if (error.response.status === 401) {
        // 切换到Login登录界面
        router.replace({
          name: 'Login'
        })
      }
      if (error.response.status === 500) {
        // 弹出elementUI的消息弹窗
        Message.error({
          message: '服务器内部异常, 请检查',
          duration: 1000
        })
      }
    } catch (e) {
      Message.error({
        message: '服务器连接超时，请重试',
        duration: 1000
      })
    }
  });


// ------------------------------------- user api -------------------------------------------
export const register = params => {
  return axios.post('/api/user/register/', params).then(res => res.data)
};

export const login = params => {
  return axios.post('/api/user/login/', params).then(res => res.data)
};


// ------------------------------------- waykichain api ---------------------------------------

// project -------------------------------------------------------------------------------------------------------------
export const addProject = body => {
  return axios.post('/api/waykichain/project/', body).then(res => res.data)
};

export const deleteProject = data => {
  return axios.delete('/api/waykichain/project/' + data.id + "/", {"data": data}).then(res => res.data)
};

export const updateProject = body => {
  return axios.patch('/api/waykichain/project/' + body.id + "/", body).then(res => res.data)
};

export const getProjectList = params => {
  return axios.get('/api/waykichain/project/', {"params": params}).then(res => res.data)
};

export const getProjectDetail = project_id => {
  return axios.get('/api/waykichain/project/' + project_id + '/').then(res => res.data)
};
// ------------------------------------------------------------------------------------------------------------- project



// api -------------------------------------------------------------------------------------------------------------
export const apiList = params => {
  return axios.get('/api/waykichain/api/', params).then(res => res.data)
};

export const getPagination_api = params => {
  return axios.get('/api/waykichain/api/', {"params": params}).then(res => res.data)
};
export const getAPIList = params => {
  return axios.get('/api/waykichain/api/', {"params": params}).then(res => res.data)
};
export const addAPI = params => {
  return axios.post('/api/waykichain/api/', params).then(res => res.data)
};

export const updateAPI = params => {
  return axios.patch('/api/waykichain/api/', params).then(res => res.data)
};

export const deleteAPI = body => {
  return axios.delete('/api/waykichain/api/', {"data": body}).then(res => res.data)
};
// -------------------------------------------------------------------------------------------------------------api



// case -------------------------------------------------------------------------------------------------------------
export const getPagination_case = params => {
  return axios.get('/api/waykichain/case/', {"params": params}).then(res => res.data)
};
export const getCaseList = params => {
  return axios.get('/api/waykichain/case/', {"params": params}).then(res => res.data)
};
export const getCaseDetail = case_id => {
  return axios.get('/api/waykichain/case/' + case_id + '/').then(res => res.data)
};

export const addCase = params => {
  console.log(params)
  return axios.post('/api/waykichain/case/', params).then(res => res.data)
};

export const deleteCase = body => {
  return axios.delete('/api/waykichain/case/', {"data": body}).then(res => res.data)
};

// ------------------------------------------------------------------------------------------------------------- case



// step -------------------------------------------------------------------------------------------------------------
export const addStep = body => {
  return axios.post('/api/waykichain/step/', body).then(res => res.data)
};

export const deleteStep = body => {
  return axios.delete('/api/waykichain/step/', {"data": body}).then(res => res.data)
};

export const updateStepAPIName = body => {
  return axios.patch('/api/waykichain/step/', body).then(res => res.data)
};
// ------------------------------------------------------------------------------------------------------------- step




// variableGlobal -----------------------------------------------------------------------------------------------------
export const addVariableGlobal = body => {
  console.log("project body: ", body)
  return axios.post('/api/waykichain/variable/', body).then(res => res.data)
};

export const deleteVariableGlobal = data => {
  return axios.delete('/api/waykichain/variable/', {"data": data}).then(res => res.data)
};

export const updateVariableGlobal = body => {
  return axios.patch('/api/waykichain/variable/', body).then(res => res.data)
};
// ---------------------------------------------------------------------------------------------------------------------



// parameter -------------------------------------------------------------------------------------------------------------
export const addParameter = body => {
  console.log("project body: ", body);
  return axios.post('/api/waykichain/parameter/', body).then(res => res.data)
};

export const deleteParameter = data => {
  return axios.delete('/api/waykichain/parameter/', {"data": data}).then(res => res.data)
};

export const updateParameter = body => {
  return axios.patch('/api/waykichain/parameter/', body).then(res => res.data)
};
// ------------------------------------------------------------------------------------------------------------- parameter



// config -------------------------------------------------------------------------------------------------------------
export const updateConfigName = body => {
  return axios.patch('/api/waykichain/config/', body).then(res => res.data)
};
// ------------------------------------------------------------------------------------------------------------- config




// validate -------------------------------------------------------------------------------------------------------------
export const addValidate = body => {
  return axios.post('/api/waykichain/validate/', body).then(res => res.data)
};
export const deleteValidate = data => {
  return axios.delete('/api/waykichain/validate/', {"data": data}).then(res => res.data)
};

export const updateValidate = body => {
  return axios.patch('/api/waykichain/validate/', body).then(res => res.data)
};
// ------------------------------------------------------------------------------------------------------------- validate




// extract -------------------------------------------------------------------------------------------------------------
export const addExtract = body => {
  return axios.post('/api/waykichain/extract/', body).then(res => res.data)
};
export const deleteExtract = data => {
  return axios.delete('/api/waykichain/extract/', {"data": data}).then(res => res.data)
};

export const updateExtract = body => {
  return axios.patch('/api/waykichain/extract/', body).then(res => res.data)
};
// ------------------------------------------------------------------------------------------------------------- extract



// runtest -------------------------------------------------------------------------------------------------------------
export const runTestcases = body => {
  return axios.post('/api/waykichain/run_test/', body).then(res => res.data)
};

// ------------------------------------------------------------------------------------------------------------- runtest




// report -------------------------------------------------------------------------------------------------------------
export const getPagination_report = params => {
  return axios.get('/api/waykichain/report/', {"params": params}).then(res => res.data)
};

export const deleteReport = report_id => {
  return axios.delete('/api/waykichain/report/' + report_id + '/').then(res => res.data)
};

export const getReportDetail = report_id => {
  return axios.get('/api/waykichain/report/' + report_id + '/').then(res => res.data)
};

export const updateReport = body => {
  return axios.patch('/api/waykichain/report/' + body.id + '/', body).then(res => res.data)
};

// ------------------------------------------------------------------------------------------------------------- report




// variableLocal ------------------------------------------------------------------------------------------------------
export const addVariableLocal = body => {
  return axios.post('/api/waykichain/variable_local/', body).then(res => res.data)
};

export const deleteVariableLocal = data => {
  return axios.delete('/api/waykichain/variable_local/', {"data": data}).then(res => res.data)
};

export const updateVariableLocal = body => {
  return axios.patch('/api/waykichain/variable_local/', body).then(res => res.data)
};
// ---------------------------------------------------------------------------------------------------------------------



//  varenv -------------------------------------------------------------------------------------------------------------
export const getPagination_varenv = params => {
  return axios.get('/api/waykichain/variable_env/', {"params": params}).then(res => res.data)
};
export const addVariableEnv = params => {
  return axios.post('/api/waykichain/variable_env/', params).then(res => res.data)
};

export const updateVariableEnv = params => {
  return axios.patch('/api/waykichain/variable_env/', params).then(res => res.data)
};

export const deleteVariableEnv = body => {
  return axios.delete('/api/waykichain/variable_env/', {"data": body}).then(res => res.data)
};

export const getBaseURLList = params => {
  return axios.get('/api/waykichain/base_url/', {"params": params}).then(res => res.data)
};
export const addBaseURL = params => {
  return axios.post('/api/waykichain/base_url/', params).then(res => res.data)
};

export const updateBaseURL  = params => {
  return axios.patch('/api/waykichain/base_url/', params).then(res => res.data)
};

export const deleteBaseURL  = body => {
  return axios.delete('/api/waykichain/base_url/', {"data": body}).then(res => res.data)
};
// ---------------------------------------------------------------------------------------------------------------------


//  Debugtalk -------------------------------------------------------------------------------------------------------------
export const getDebugtalk = params => {
    return axios.get('/api/waykichain/debugtalk/', {"params": params}).then(res => res.data)
};

export const updateDebugtalk = params => {
    return axios.patch('/api/waykichain/debugtalk/', params).then(res => res.data)
};

export const runDebugtalk = params => {
    return axios.post('/api/waykichain/debugtalk/', params).then(res => res.data)
};




