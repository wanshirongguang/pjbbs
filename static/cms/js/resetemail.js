$(function () {
    $("#btn11").click(function (ev) {
        ev.preventDefault();
        $('#btn11').attr("disabled",true);
        $.ajax({
            url:"/cms/send_email/",
            type:"post",
            data:{
                "email":$("#exampleInputEmail3").val(),
                "csrf_token":$("#csrf_token").attr("value")
            },
            success:function (data) {
                if (data.code == 200){
                    xtalert.alertSuccessToast(data.msg)
                    var timer;
                    var num = 60;
                    clearInterval(timer);
                    timer = setInterval(function () {
                        num--;
                        if (num<=0){
                            clearInterval(timer);
                            $('#btn11').attr("disabled",false);
                            $("#btn11").html("重新发送")
                        }else {
                            $("#btn11").html(num+"s后重新发送")
                        }
                    },1000)
                }else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });
    $("#btn").click(function (ev) {
        ev.preventDefault();
        $.ajax({
            url:"/cms/reseteamil/",
            type:"post",
            data:{
                "email":$("#exampleInputEmail3").val(),
                "code":$("#exampleInputPassword3").val(),
                "csrf_token":$("#csrf_token").attr("value")
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast(data.msg)
                }else {
                    xtalert.alertErrorToast(data.msg)
                }

            }
        })
    })

});