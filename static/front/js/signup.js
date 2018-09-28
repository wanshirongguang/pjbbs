$(function () {
    $("#send_sms_code_btn").click(function (ev) {
        ev.preventDefault();
        $.ajax({
            url:"/send_sms_code/",
            type:"post",
            data:{
              "telephone" :$("#telephone").val(),
              "csrf_token":$("#csrf_token").attr("value")
            },
            success:function (data) {
                if(data.code == 200 ){
                    xtalert.alertSuccessToast(data.msg)
                    var timer;
                    var num = 60;
                    $('#send_sms_code_btn').attr("disabled",true);
                    clearInterval(timer);
                    timer = setInterval(function () {
                        num--;
                        if (num<=0){
                            clearInterval(timer);
                            $('#send_sms_code_btn').attr("disabled",false);
                            $("#send_sms_code_btn").html("重新发送")
                        }else {
                            $("#send_sms_code_btn").html(num+"s后重新发送")
                        }
                    },1000)
                }else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });

    $(".captcha").click(function (ev) {
        ev.preventDefault();
        r = Math.random();
        self = $(".captcha");  // 把js的self变成jq的self
        url = self.attr('data-src') + '?a=' + r ; //    /img_code/?a=随机数
        self.attr("src",url);
    });

    $("#signup_btn").click(function (ev) {
        ev.preventDefault();
        $.ajax({
            url:"/signup/",
            type:"post",
            data:{
                "csrf_token":$("#csrf_token").attr("value"),
                "telephone":$("#telephone").val(),
                "smscode":$("#smscode").val(),
                "username":$("#username").val(),
                "password":$("#password").val(),
                "password1":$("#password1").val(),
                "captchacode":$("#captchacode").val()
            },
            success:function (data) {
                if(data.code == 200){
                    xtalert.alertSuccessToast(data.msg);
                    window.location = "/";
                }else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    })

});