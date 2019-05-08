export default {

    isLogin(state, value) {
        state.token = value;
    },
    setUser(state, value) {
        state.user = value;
    },
    setRouterName(state, value) {
        state.routerName = value
    },
    setfileConent(state, value) {
        state.fileConent = value
    },
    setCurrentCase(state, value) {
        state.currentCase = value
    },
    setCaseList(state, value) {
        state.caseList = value
    }
}
