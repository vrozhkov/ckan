function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('#inp-image').show();
            $(input).hide();
            $('#inp-image').attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}
$(document).ready(function(){
    var maxLength = 50;
	$(".show-read-more").each(function(){
		var myStr = $(this).text();
		if($.trim(myStr).length > maxLength){
			var newStr = myStr.substring(0, maxLength);
			var removedStr = myStr.substring(maxLength, $.trim(myStr).length);
			$(this).empty().html(newStr);
			$(this).append(' <a href="javascript:void(0);" class="read-more">read more...</a>');
			$(this).append('<span class="more-text">' + removedStr + '</span>');
		}
	});
	$(".read-more").click(function(){
		$(this).siblings(".more-text").contents().unwrap();
		$(this).remove();
	});
});

