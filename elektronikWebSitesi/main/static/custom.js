$(document).ready(function(){
    $("#loadMore").on('click',function(){
        var _currentProducts=$(".product-box").length;
		var langTrValue = 0
		var langEnValue = 0
		
		if(document.getElementById('lang-1').checked){
			langTrValue = document.getElementById('lang-1').value
		}

		if(document.getElementById('lang-2').checked){
			langEnValue = document.getElementById('lang-2').value
		}

		if(document.getElementById)

		
		var _limit=$(this).attr('data-limit');
		var _total=$(this).attr('data-total');


        $.ajax({
			url:'/load-more-data',
			data:{
				limit:_limit,
				offset:_currentProducts,
				langTrValue:langTrValue,
				langEnValue:langEnValue
			},
			dataType:'json',
			beforeSend:function(){
				$("#loadMore").attr('disabled',true);
                $(".load-more-icon").addClass('fa-spin');
			},
			success:function(res){
				$("#filteredProducts").append(res.data);
                
				$("#loadMore").attr('disabled',false);
				$(".load-more-icon").removeClass('fa-spin');

				var _totalShowing=$(".product-box").length;
				if(_totalShowing==_total){
					$("#loadMore").remove();
                }
			}
		});








    });
});