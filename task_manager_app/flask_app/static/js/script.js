const element = document.querySelectorAll('#statusSelect')
$(element).change(function () {
    var selectedId = $('option:selected', this).attr('id');
    console.log(selectedId)
    if (selectedId == "pending") {
        jQuery(this).attr("class","badge bg-danger");}
    if (selectedId == "complete") {
        jQuery(this).attr("class","badge bg-success");}
    if (selectedId == "working") {
        jQuery(this).attr("class","badge bg-warning");
    }
});

// $(document).ready(function () {

//     if (localStorage.getItem("my_app_name_here-quote-scroll") != null) {
//         $(window).scrollTop(localStorage.getItem("my_app_name_here-quote-scroll"));
//     }

//     $(window).on("scroll", function() {
//         localStorage.setItem("my_app_name_here-quote-scroll", $(window).scrollTop());
//     });

    // });
    function toggle(source) {
        checkboxes = document.getElementsByName('checked1');
        for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
        }
    }
        function toggle2(source) {
        checkboxes = document.getElementsByName('complete');
        for(var i=0, n=checkboxes.length;i<n;i++) {
        checkboxes[i].checked = source.checked;
        }
    }

    function disableButton(button) {
        button.disabled = true;
        button.value = "submitting...."
        button.form.submit();
    }





    // menu for anouncements//

    function changeLanguage(language) {
        var element = document.getElementById("url");
        element.value = language;
        element.innerHTML = language;
      }
      
      function showDropdown() {
        document.getElementById("menumyDropdown").classList.toggle("menushow");
      }
      
      // Close the dropdown if the user clicks outside of it
      window.onclick = function(event) {
        if (!event.target.matches(".menudropbtn")) {
          var dropdowns = document.getElementsByClassName("menudropdown-content");
          var i;
          for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains("menushow")) {
              openDropdown.classList.remove("menushow");
            }
          }
        }
      };
      