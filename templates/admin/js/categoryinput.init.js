$(function () {
    // 将数据传输到修改弹框里
    $('.update_category_btn').on('click', function () {
        var old_category = $(this).parents("tr").children(".category_data").text()
        $('#update_input').val(old_category)
        $('#update_input_old').val(old_category)
    });
    // 将数据传输到删除弹框里
    $('.delete_Btn').on('click', function () {
        var delete_category = $(this).parents("tr").children(".category_data").text()
        $('#delete_category_data').val(delete_category)
    });
    // 初始化弹窗插件
    const Toast = Swal.mixin({
        toast: true,
        position: 'center',
        showConfirmButton: true,
        timer: 3000
    });

    //修改弹框Ajax
    $('#updateCategoryBtn').on('click', function (e) {
        $("input").attr("disabled", "disabled");
        var event = e || window.event;
        if (event.preventDefault) {
            event.preventDefault();
        } else {event.returnValue = false;}
        e.stopPropagation()
        $.ajax({
            type: "post",
            url: "./category_manager/update_category", //换成这个接口
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                category_old: $("#update_input_old").val(),
                category_new: $("#update_input").val(),
            }),
            success: function (data) {
                if (data['msg'].indexOf('成功') != -1) {
                    Toast.fire({
                        icon: 'success',
                        title: data['msg']
                    });

                } else {
                    Toast.fire({
                        icon: 'error',
                        title: data['msg']
                    });
                }
            }
        })
    setTimeout(function () {
                location.reload()
            }, 1000);
    })

    //删除弹框Ajax
    $('#deleteCategoryBtn').on('click', function (e) {
        $("input").attr("disabled", "disabled");
        var event = e || window.event;
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false;
        }
        e.stopPropagation()
        $.ajax({
            type: "post",
            url: "./category_manager/delete_category", //换成这个接口
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                category_delete: $("#delete_category_data").val(),
            }),
            success: function (data) {
                if (data['msg'].indexOf('成功') != -1) {
                    Toast.fire({
                        icon: 'success',
                        title: data['msg']
                    });
                } else {
                    Toast.fire({
                        icon: 'error',
                        title: data['msg']
                    })
                }
            }
        })
        setTimeout(function () {
                    location.reload()
                }, 1500);
    })

    //初始化分类输入框
    $('#categoryInput').selectize({
        create: true,
        createOnBlur: true,
        maxItems: 10
    });

    //新增分类按钮事件
    $('#addCategoryBtn').on('click', function () {
        alert($('#categoryInput').val().split(','));
    });
});