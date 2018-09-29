$(function () {
    $("#saveBanner").click(function (ev) {
        ev.preventDefault();
        var saveoradd = $(this).attr('from');
        if  (saveoradd == 1){
            var url = "/cms/updatebanner/";
        }else {
            url = "/cms/addbanner/";
        }
        $.ajax({
            url:url,
            type:"post",
            data :{
                "csrf_token":$("#csrf_token").attr("value"),
                "bannerName":$("#bannerName").val(),
                "imglink":$("#imglink").val(),
                "link":$("#link").val(),
                "priority":$("#priority").val(),
                "id":$("#id").val(),
            },
            success:function (data) {
                if (data.code == 200){
                    xtalert.alertSuccessToast(data.msg);
                    window.location = "/cms/banner/"
                }else {
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });

    $('.update-btn').click(function () {
        self = $(this);
        $('#myModal').modal('show');// 让模态框出来
        $('meta[name=csrf_token]').attr("value");
        $("#bannerName").val(self.attr('data-bannerName'));
        $('#imglink').val(self.attr('data-imglink'));
        $('#link').val(self.attr('data-link'));
        $('#priority').val(self.attr("data-priority"));
        $('#saveBanner').attr("from",'1');
        $('#id').val(self.attr('data-id'));
    });
     $('#myModal').on('hidden.bs.modal', function (e) {
         e.preventDefault();
         $('#saveBanner').attr("from",'0')
    });

    $('.delete-btn').click(function (ev) {
        ev.preventDefault();
         $.ajax({
            url:'/cms/deletebanner/',
            type:'post',
            data:{
                'csrf_token':$("#csrf_token").attr("value"),
                'id':$(this).attr('data-id')
            },
            success:function (data) {
                if (data.code == 200) {
                    xtalert.alertSuccessToast("删除成功");
                    window.location.reload(); //  重新加载这个页面
                } else {  // 提示出错误
                    xtalert.alertErrorToast(data.msg)
                }
            }
        })
    });
    uploader = Qiniu.uploader({
            runtimes: 'html5,html4,flash',
            browse_button: 'btnbtn',//上传按钮的ID,
            max_file_size: '4mb',//最大文件限制
            dragdrop: false, //是否开启拖拽上传
            uptoken_url: '/cms/qiniu_token/',//设置请求qiniu-token的url
            domain: 'pfpjd7i5o.bkt.clouddn.com',//自己的七牛云存储空间域名
            get_new_uptoken: false, //是否每次上传文件都要从业务服务器获取token
            auto_start: true, //如果设置了true,只要选择了图片,就会自动上传
            unique_names: true,
            multi_selection: false,//是否允许同时选择多文件
            //文件类型过滤，这里限制为图片类型
            filters: {
              mime_types : [
                {title : "Image files", extensions: "jpg,jpeg,png"}
              ]
            },
            init: {
                'FileUploaded': function(up, file, info) {
                   var domain = up.getOption('domain');
                   var res = eval('(' + info + ')');
                    res.key;//获取上传文件的链接地址
                   // $('#imglink').attr('value',sourceLink)
                    sourceLink = 'http://pfpjd7i5o.bkt.clouddn.com/' + res.key;
                    // 放到我们的input标签中
                    $("#imglink").val(sourceLink);
                },
                'Error': function(up, err, errTip) {
                    console.log(err);
                    xtalert.alertErrorToast("上传失败")
                }
            }
        })


});
