$(function () {

    const Toast = Swal.mixin({
        toast: true,
        position: 'center',
        showConfirmButton: true,
        timer: 3000
    });


    $('#skill').selectize({
        create: true,
        createOnBlur: true,
        maxItems: 10
    });

    $('#hobby').selectize({
        create: true,
        createOnBlur: true,
        maxItems: 10
    });

    $('#update-userdate').click(function (e) {
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
            url: "/admin/configuration/update_user",
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify({
                username: $("#username").val(),
                nickname: $("#nickname").val(),
                email: $("#email").val(),
                head_portrait: $("#head_portrait").val(),
                phone_num: $("#phone_num").val(),
            }),
            success: function (data) {
                Toast.fire({
                    icon: 'success',
                    title: data['msg']
                });
            }
        })
        setTimeout(function () {
            location.reload()
        }, 2500);
    })
});