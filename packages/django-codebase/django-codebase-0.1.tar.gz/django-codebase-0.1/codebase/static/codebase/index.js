$(document).ready(function(){
    console.log("d")
    //~ alert("d")
    
    
    keys = ["k1","k2","k3","k4","k5"]
    values = ["v1","v2",{"k3":"v3","k4":"v4"},["v5","v6","v7"],"abc|def"]
    
    var obj = {}
    $.each(keys,function(index,item){
	
	
	obj[item] = values[index]
	
	
	
	
    })
    
    console.log(obj)
	
	
	
     $.ajax({
	url : '/codebase/a_get_apis/',
	type : "GET",
	success : function(json){
	    
	    $.each(json["response"],function(api){
		
		$('.url').append('<ul>'+api["url"]+'</ul><br>')
		
	    })
		
	}
    })   




    $('body').on('click','.hit_api',function(){
	
	url = 'a_get_apis'
	http_type = "GET"
	    
	$.ajax({
	    url : url,
	    type : http_type,
	    success:function(json){
		
		var jsonStr = json;
		//~ var jsonObj = JSON.parse(jsonStr);
		var jsonPretty = JSON.stringify(json, null, '\t');
	    
		$(".api-result").text(jsonPretty);
		
	}
    })

	
	
    })



})
