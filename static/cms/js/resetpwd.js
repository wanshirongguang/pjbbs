$(function () {
    $(".btn").click(function (ev) {
        ev.preventDefault();
        console.log($("#oldpassword").val());
        console.log($("#newpassword1").val());
        $.ajax({
            url:"/cms/resetpwd/",
            type:"post",
            data:{
                "oldpassword":$("#oldpassword").val(),
                "newpassword1":$("#newpassword1").val(),
                "newpassword2":$("#newpassword2").val(),
                "csrf_token":$("#csrf_token").attr("value")
            },
            success:function (data) {
                if (data.code == 200){
                    xtalert.alertSuccessToast(data.msg);
                    $("#oldpassword").val("");
                    $("#newpassword1").val("");
                    $("#newpassword2").val("");
                }else {
                    xtalert.alertErrorToast(data.msg);
                }
            }
        })
    })
});