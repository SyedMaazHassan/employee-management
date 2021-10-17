$("#reset-password-form").on("submit", function (event) {
    let email = $("#id_email").val();
    if (email && email.length > 0) {
        $.ajax({
            url: myURL,
            type: "GET",
            data: `email=${email}`,
            success: (response)=>{
                if (response.status) {
                    $("#error").text("");
                    // $("#reset-password-form").submit();
                    $("#submit_btn").click();
                }else{
                    $("#error").text(response.message);
                    event.preventDefault();
                }
            },
            error: (response)=>{
                $("#error").text(response.message)
                event.preventDefault();
            },
            async: false
        });
        // event.preventDefault();
    }else{
        event.preventDefault();
    }
});