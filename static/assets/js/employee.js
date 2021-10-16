var is_already_open = false;
var to_open = false;

function openNav() {
    if (!(is_already_open)) {
        to_open = true;
    }
    document.getElementById("mySidenav").style.width = "400px";
    $("#mySidenav").css('box-shadow', '10px 10px 10px 15px #cccccc');
    is_already_open = true;
    // Check browser support
    if (typeof(Storage) !== "undefined") {
        // Store
        localStorage.setItem("add_employee", "true");
    }
}

function closeNav() {
    if (to_open) {
        openNav();
        to_open = false;
        return;
    }
    console.log("closed clicked");
    document.getElementById("mySidenav").style.width = "0";
    $("#mySidenav").css('box-shadow', 'none');
    is_already_open = false;
    if (typeof(Storage) !== "undefined") {
        // Store
        localStorage.setItem("add_employee", "false");
    }
}

document.addEventListener("click", function(e){
    var a = e.target;
    var els = [];
    while (a) {
        els.unshift(a.id);
        a = a.parentNode;
    }

    if (!(els.includes("mySidenav")) && !(els.includes("newTranslation"))) {
        closeNav();
    }
});



function open_id_card(data, counter, modal=true) {
    let employee = JSON.parse(data);
    $("#qr-loading").show();

    selected_employee = employee;

    $("#company-name").text(employee.company.name);
    $("#company-tagline").text(employee.company.tagline);
    $("#employee-picture").attr("src", `media/${employee.profile_picture}`);
    $("#employee-show-id").text(`C${employee.company.id}E${counter}`);
    $("#employee-name").text(employee.name);
    $("#employee-email").text(employee.email);
    $("#employee-designation").text(employee.designation);

    $("#employee-phone").text(employee.phone);
    $("#employee-date-joined").text(employee.date_joined);
    
    // $("#qr-loading").text(employee.company.name);
    generateQRCode(employee.id);
    $("#qr-container").hide();  
    
    if (modal) {
        $("#id-card-modal").modal("show");
    }

    setTimeout(() => {
        $("#qr-container").show();
        $("#qr-loading").hide();

    }, 700);


}

function generateQRCode(myqrtext) {
    let protocol = window.location.protocol;
    let host = window.location.host;
    let url = `${protocol}//${host}/employee/${myqrtext}`;

    $("#qr-container").html("");
    let qr_container = document.getElementById("qr-container");
    var qrcode = new QRCode(qr_container, {
        text: url,
        width: 80,
        height: 80,
        colorDark : "#000000",
        colorLight : "#ffffff",
        correctLevel : QRCode.CorrectLevel.H
    });
}


function print_card(selected_employee){
    if (selected_employee) {
        let filename = `${selected_employee.filename}`;
        console.log(selected_employee);
        let card = document.getElementById("myIdCard");
        html2pdf()
        .set({
            margin: [15, 40, 15, 40], 
            filename: filename,
            image: { type: 'jpeg', quality: 1 },
            html2canvas: {
                dpi: 192,
                scale:4,
                letterRendering: true,
                useCORS: true
            },
        })
        .from(card)
        .save();            
    }
}



$("#download_btn").on("click", function () {
    print_card(selected_employee);
});
