function parseXml(xmlstr)
		{
			var doc = new DOMParser().parseFromString(xmlstr, "text/xml");
			return get_gpx_data(doc.documentElement);
		}
	
		function get_gpx_data(node, result) {
			if(!result)
				result = { segments: [] };
				
			switch(node.nodeName)
			{
				case "name":
					var p = $("<p />");
					p.text(node.nodeName + " = " + node.textContent);
					result.name = node.textContent;
					$("#log").append(p);
					break;
					
				case "trkseg":
					var segment = [];
					result.segments.push(segment)
					for(var i=0; i<node.childNodes.length; i++)
					{
						var snode = node.childNodes[i];
						if(snode.nodeName == "trkpt")
						{
							var trkpt = { loc: [ parseFloat(snode.attributes["lat"].value), parseFloat(snode.attributes["lon"].value) ] };
							for(var j=0; j<snode.childNodes.length; j++)
							{
								var ssnode = snode.childNodes[j];
								switch(ssnode.nodeName)
								{
									case "time":
										trkpt.time = new Date(ssnode.childNodes[0].data);
										break;
									case "ele":
										trkpt.ele = parseFloat(ssnode.childNodes[0].data);
										break;
								}
							}
							segment.push(trkpt)
						}
					}
					break;
			}
		
			for(var i=0; i<node.childNodes.length; i++)
			{
				get_gpx_data(node.childNodes[i], result);
			}
			return result;
		}
		
		function convert_to_latlng(segment)
		{
			var result = [];
			for(var i=0; i<segment.length; i++)
			{
				result.push(new google.maps.LatLng(segment[i].loc[0], segment[i].loc[1]));
			}
			return result;
		}
		
		function get_bounds(gpx_data)
		{
			var result = { s: 90.0, n: -90, e: -180.0, w: 180.0 };
			for(var i=0; i<gpx_data.segments.length; i++)
			{
				for(var j=0; j<gpx_data.segments[i].length; j++)
				{
					var point = gpx_data.segments[i][j];
					if(result.s > point.loc[0]) result.s = point.loc[0];
					if(result.n < point.loc[0]) result.n = point.loc[0];
					if(result.e < point.loc[1]) result.e = point.loc[1];
					if(result.w > point.loc[1]) result.w = point.loc[1];
				}
			}	
			return result;
		}