/*global opener */
(function() {
    'use strict';
    var popupResponse = document.getElementById('django-admin-popup-response-constants').dataset.popupResponse
    var initData
    try {
        initData = JSON.parse(popupResponse);
        switch(initData.action) {
        case 'change':
            opener.dismissChangeRelatedObjectPopup(window, initData.value, initData.obj, initData.new_value);
            break;
        case 'delete':
            opener.dismissDeleteRelatedObjectPopup(window, initData.value);
            break;
        default:
            opener.dismissAddRelatedObjectPopup(window, initData.value, initData.obj);
            break;
        }   
    } catch (err) {
        console.error("error retrieving popup response")
    }
})();
