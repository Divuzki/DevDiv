// DevDiv Since 2020
[].forEach.call(document.getElementById("div_id_hashtag").getElementsByTagName("div"), function (el) {
  el.classList.add("tags-input");
  el.setAttribute('data-name', 'hashtags');

    let hiddenInput   = document.createElement("input"),
        mainInput     = document.getElementById("id_hashtag"),
        tags = [];
    
    hiddenInput.setAttribute('type', 'hidden');
    hiddenInput.setAttribute('id', 'hashtags');
    hiddenInput.setAttribute('name', el.getAttribute('data-name'));

    mainInput.setAttribute('type', 'text');
    mainInput.setAttribute('name', '');
    mainInput.classList.add('main-input');
    mainInput.classList.remove('form-control');
    mainInput.addEventListener('input', function () {
        let enterTags = mainInput.value.split(' ');
        if (enterTags.length > 1) {
            enterTags.forEach(function (t) {
                let filteredTag = filterTag(t);
                if (t.charAt(0) == "#") {
                    if (filteredTag.length > 0){
                        filteredTag = filterTag(filteredTag);
                        filteredTag = "#" + filteredTag;
                        addTag(filteredTag);
                    }
                }
                else{
                    hashtag_field.placeholder = "#";
                }
            });
            mainInput.value = '';
        }
    });

    mainInput.addEventListener('keydown', function(e) {
        let keyCode = e.which || e.keyCode;
        if (keyCode === 8 && mainInput.value.length === 0 && tags.length > 0)
                removeTag(tags.length -1);
    });

    el.appendChild(mainInput);
    el.appendChild(hiddenInput);

    function addTag (text) {
        let tag = {
            text: text,
            element: document.createElement('span'),
        }
        tag.element.classList.add("tag");
        tag.element.textContent = tag.text;

        let closeBtn = document.createElement("span");
        closeBtn.classList.add('clse');
        closeBtn.addEventListener('click', function () {
            removeTag(tags.indexOf(tag));
        });
        tag.element.appendChild(closeBtn);

        tags.push(tag);

        el.insertBefore(tag.element, mainInput);

        refreshTags();
    }

    function removeTag (index) {
        let tag = tags[index];
        tags.splice(index, 1);
        el.removeChild(tag.element);
        refreshTags();
    }
    function refreshTags () {
        let tagsList = [];
        tags.forEach(function (t) {
            tagsList.push(t.text);
        });
        hiddenInput.value = tagsList.join(',');
        var form = $(this).closest("form");
        let tagtitle = document.getElementById("id_title");
        if (hiddenInput.value.charAt(0) == "#" && hiddenInput.value.length > 2) {
        $.ajax({
            method: "POST",
            url: "/hashtag/",
            data: {
            name: hiddenInput.value,
            post: tagtitle.value,
            csrfmiddlewaretoken: form.attr("token")
            },
            dataType: 'json',
        });
        } else {
        if (hiddenInput.value == "" || null) {
            console.log("UVV0L '#' IN SERVER CLOUD");
        } else {
            alert("This is a hashtag, You need to add the symbol '#' in " + hiddenInput.value + "");
        }
        }
    }
    function filterTag (tag) {
        return tag.replace(/[^\w -]/g, '#').trim().replace(/\W+/g, '');
    }
});

//JQuery
 // HashTag
  $("#id_form").on("submit", function (e) {
    var form = $(this).closest("form");
    var tagtitle = document.getElementById("id_title");
    if ($('#id_hashtag').val().charAt(0) == "#" && $('#id_hashtag').val().length >= 2) {
      $.ajax({
        method: "POST",
        url: "/hashtag/",
        data: {
          name: $('#hashtags').val(),
          post: tagtitle.value,
          csrfmiddlewaretoken: form.attr("token")
        },
        dataType: 'json',
      });
    } else {
      if ($('#id_hashtag').val() == "" || null) {
        console.log("UVV0L '#' IN SERVER CLOUD");
      } else {
        alert("This is a hashtag, You need to add the symbol '#' in " + $('#id_hashtag').val() + "")
      }
    }
});

// HashTag Autocomplete
$('#id_hashtag').on('input', function () {
    function split( val ) {
      return val.split( /,\s*/ );
    }
    $(this).autocomplete({
      minLength: 2,
      source: '/hashtag/',
      select: function( event, ui ) {
        var terms = split( this.value );
        // remove the current input
        terms.pop();
        // add the selected item
        terms.push( ui.item.value );
        // add placeholder to get the comma-and-space at the end
        terms.push( "" );
        this.value = terms.join( "" );
        return false;
      },
      maxResults: 5,
      _renderItem: function( ul, item) {
        return $( "<li></li>" )
            .data( "item.autocomplete", item )
            .append( "<a>" + item.label + "</a>" )
            .appendTo( ul );
    },
    });
  });
  $(".ui-menu-item").click(function() {
    var e = $.Event('keypress');
    e.which = 9;
    this.trigger(e);
  });