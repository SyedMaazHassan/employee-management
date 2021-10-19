function upload_picture(input_id){
    $("#"+input_id).click();
}


function readURL(input, show, big=false) {
    $("#"+show).css('display', 'none');
    nameFile = input.files[0].name.split(".");
    nameFile = nameFile[nameFile.length-1];
    
    console.log(nameFile);
    if(nameFile=="png" || nameFile=="jpg" || nameFile=="jpeg" || nameFile=="JPG"){
        if (input.files && input.files[0]) {
            $("#file-error-msg").text("");

            var reader = new FileReader();

            reader.onload = function (e) {
                var result_to_show = e.target.result;
                console.log(result_to_show)

                if (big) {
                    $("#"+show).css('display', '');
                    $("#"+show).prop("class", "decrease-s-width");
                    $('#'+show)
                        .attr('src', result_to_show)
                        .width("100%")
                        .height('');
                }else{
                    $("#"+show).css('display', '');
                    $("#"+show).prop("class", "decrease-s-width");
                    $('#'+show)
                        .attr('src', result_to_show)
                        .css('border-radius', '100%')
                        .width(100)
                        .height('');
                }

               

                // $("#preview").modal("show");
                $("#showing_div").show();
                $("#image_error").hide();
            };

            if (!(nameFile == "docx" || nameFile == "doc")) {
                $("#see_docs_file").css('display', 'none');
                reader.readAsDataURL(input.files[0]);
            }else{
                $("#see_docs_file").css('display', '');
                reader.readAsDataURL(input.files[0]);
            }

            $("#success-msg").css('display', '');

        }
    }else{
        alert("Upload only image (in PNG, JPEG, JPG etc)");
        $("#employee_profile_picture_show").show();
    }
}