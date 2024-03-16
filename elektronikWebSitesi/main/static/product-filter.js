$(document).ready(function(){
    $(".ajaxLoader").hide();
    
    $(".filter-checkbox,#priceFilterBtn").on('click',function(){
        var _filterObj={};
        var _minPrice=$('#maxPrice').attr('min');
        var _maxPrice=$('#maxPrice').val();
        _filterObj.minPrice=_minPrice;
        _filterObj.maxPrice=_maxPrice;
       
        $(".filter-checkbox").each(function(index,ele){
           var _filterVal=$(this).val();
           var _filterKey=$(this).data('filter');
            _filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(
                function(el){
                    return el.value;

            });
        });




        $.ajax({
            url:'/filter-data',
            
            data:_filterObj,
            dataType:'json',
            beforeSend:function(){
                $(".ajaxLoader").show();

            },
            success:function(res){
                console.log(res)
                $("#filteredProducts").html(res.data);
                $(".ajaxLoader").hide();

                
            }
         });
       
    });





});