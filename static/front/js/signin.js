$(function () {
    $("#signin_btn").click(function (ev) {
        console.log($('meta[name=from]').attr('value'));
        ev.preventDefault();
        $.ajax({
            url:"/signin/",
            type:"post",
            data:{
                "csrf_token":$("#csrf_token").attr("value"),
                "telephone":$("#telephone").val(),
                "password":$("#password").val(),
                "rember":$("#remberme").prop("checked")?1:2
            },
            success:function (data) {
                if(data.code == 200){
                    xtalert.alertSuccessToast(data.msg);
                    window.location = $('meta[name=from]').attr('value')
                }else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    })

});