var myutils = {
    isUrl: function(url){
    	var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
    	return regexp.test(url);
    },

    isEmail: function(email){
        var regex = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return regex.test(email);
    },

    //fades the notification out
    autoHideAlert: function(elID){
        setTimeout(function(){
            $('#'+elID).fadeOut(700);
        },3000);
    },

    //fades the notification out
    showConAlert: function(elID){
        $('#'+elID).show();
    },

    //Confirmation modal
    confirmAction: function(msg, size, title, btns, icon, baseurl){
        var modalSize = "";
        var modalSizeH = "";
        var negativeBtn = 'button type="button" class="btn btn-default" data-dismiss="modal">Close</button>';
        var positiveBtn = 'button type="button" class="btn btn-default" data-dismiss="modal">Okay</button>';

        if(size==="small"){
            modalSize = "modal-sm";
            modalSizeH = "bs-example-modal-sm";
        }

        if(size==="large"){
            modalSize = "modal-lg";
            modalSizeH = "bs-example-modal-lg";
        }

        var countbtn = 0;
        $.each(btns, function(i, val){
            if(val.toLowerCase()==="close" || val.toLowerCase()==="cancel" || val.toLowerCase()==="no"){
                negativeBtn = '<button type="button" class="btn btn-secondary" data-dismiss="modal">'+val+'</button>';
            }
            if(val.toLowerCase()==="okay" || val.toLowerCase()==="save" || val.toLowerCase()==="save changes" || val.toLowerCase()==="save entry" || val.toLowerCase()==="yes" || val.toLowerCase()==="confirm"){
                if(icon==="error" || icon==="success"){
                    positiveBtn = '<button type="button" class="btn btn-primary" data-dismiss="modal">'+val+'</button>';
                }else{
                    positiveBtn = '<button type="button" class="btn btn-primary btnCallBack">'+val+'</button>';
                }
            }
            countbtn++;
        });

        if(countbtn===1){
            negativeBtn = "";
        }

        switch(icon){
            case "error":
                icon = baseurl+"error.png";
                break;

            case "warning":
                icon = baseurl+"warning.png";
                break;

            case "success":
                icon = baseurl+"success.png";
                break;

            case "ask":
                icon = baseurl+"ask.png";
                break;

            default:
                icon = baseurl+"error.png";
        }

        icon = '<div class="float-left image"><img src="'+icon+'" style="width:40px;margin-right:6px;" class="img-circle" alt="Image"/></div>';

        var modalElem = `<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered" role="document">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="exampleModalLongTitle">`+title+`</h5>
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        `+ icon + msg +`
                                    </div>
                                    <div class="modal-footer">
                                        `+negativeBtn+positiveBtn+`
                                    </div>
                                </div>
                            </div>
                        </div>`;

        $("#divContentWrapper").html("");
        $(modalElem).appendTo("#divContentWrapper");
        $("#divContentWrapper").show();
        $("#myModal").modal();

        $(".btnCallBack").click(function(){
            $("#myModal").modal('hide');
                eval(gCallback);
        });
    },

    //Notify message on top right of the screen
    my_notify: function(icon, title, msg, common_assets){
        var mTemplate = '';

        switch(icon){
            case "error":
                icon = common_assets+"error.png";
                mTemplate = `<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert" style="z-index:9999; color: #721c24; background-color: #f8d7da; border-color: #f5c6cb; !important;">
                    <img data-notify="icon" class="rounded-circle float-left">
                    <div data-notify="title" style="font-size:18px;color:#000;">{1}</div>
                    <div data-notify="message" style="font-size:14px;color:#707273">{2}</div></div>
                </div>`;
                break;

            case "warning":
                icon = common_assets+"warning.png";
                mTemplate = `<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert" style="z-index:9999; color: #856404; background-color: #fff3cd; border-color: #ffeeba; !important;">
                    <img data-notify="icon" class="rounded-circle float-left">
                    <div data-notify="title" style="font-size:18px;color:#000;">{1}</div>
                    <div data-notify="message" style="font-size:14px;color:#707273">{2}</div></div>
                </div>`;
                break;

            case "success":
                icon = common_assets+"success.png";
                mTemplate = `<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert" style="z-index:9999; color: #155724; background-color: #d4edda; border-color: #c3e6cb; !important;">
                    <img data-notify="icon" class="rounded-circle float-left">
                    <div data-notify="title" style="font-size:18px;color:#000;">{1}</div>
                    <div data-notify="message" style="font-size:14px;color:#707273">{2}</div></div>
                </div>`;
                break;

            case "info":
                icon = common_assets+"info.png";
                mTemplate = `<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert" style="z-index:9999; color: #0c5460; background-color: #d1ecf1; border-color: #bee5eb; !important;">
                    <img data-notify="icon" class="rounded-circle float-left">
                    <div data-notify="title" style="font-size:18px;color:#000;">{1}</div>
                    <div data-notify="message" style="font-size:14px;color:#707273">{2}</div></div>
                </div>`;
                break;

            default:
                icon = common_assets+"info.png";
        }

        $.notify({
            icon: icon,
            title: title,
            message: msg
        },{
            type: 'minimalist',
            delay: 5000,
            icon_type: 'image',
            template: mTemplate
        });
    },

    // Auto update timeago
    updateLocalTime: function(){
        $(".timeago").each(function() {
            var testDateUTC = moment.utc($(this).attr('datetime'));
            var localDate = moment(testDateUTC).local();
            $(this).attr('datetime', localDate.format("YYYY-MM-DD HH:mm:ss"));
        });

        var timeagoInstance = timeago();
        var nodes = document.querySelectorAll('.timeago');
        // use render method to render nodes in real time
        timeagoInstance.render(nodes);
    },

    // Auto update timeago for ws data only
    updateLocalTimeWS: function(){
        $(".timeago_ws").each(function() {
            var testDateUTC = moment.utc($(this).attr('datetime'));
            var localDate = moment(testDateUTC).local();
            $(this).attr('datetime', localDate.format("YYYY-MM-DD HH:mm:ss"));
        });

        var timeagoInstance = timeago();
        var nodes = document.querySelectorAll('.timeago');
        // use render method to render nodes in real time
        timeagoInstance.render(nodes);
    },

    // Fades the notification out
    hideOnClick: function(elID){
        $('#'+elID).on('click', function(){
        	$(this).fadeOut(700);
        });
    },

    // Show tooltip
    showToolTip: function(){
        $('[data-toggle="tooltip"]').tooltip();
    },

    // Google reCAPTCHA
    btnReCaptcha: function(elID){
        var element = document.getElementById(elID);
        element.onclick = validate;
    },

    // Datatable object
    dataTableConfig: function(elID){
        $('#'+elID).DataTable({
	      'paging'      : true,
	      'lengthChange': false,
	      'searching'   : false,
	      'ordering'    : true,
	      'info'        : true,
	      'autoWidth'   : true,
          'deferRender': true
        });
    },
}
