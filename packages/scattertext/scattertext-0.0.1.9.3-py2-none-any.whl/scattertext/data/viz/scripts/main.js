function buildViz(widthInPixels = 800,
                  heightInPixels = 600,
                  max_snippets = null) {
    var divName = 'd3-div-1';

    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = widthInPixels - margin.left - margin.right,
        height = heightInPixels - margin.top - margin.bottom;

    // Set the ranges
    var x = d3.scaleLinear().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    function axisLabeler(d, i) {
        return ["Infrequent", "Average", "Frequent"][i]
    }

    var xAxis = d3.axisBottom(x).ticks(3).tickFormat(axisLabeler);

    var yAxis = d3.axisLeft(y).ticks(3).tickFormat(axisLabeler);

    // var label = d3.select("body").append("div")
    var label = d3.select('#' + divName).append("div")
        .attr("class", "label");

    // setup fill color
    var color = d3.interpolateRdYlBu;

    // Adds the svg canvas
    // var svg = d3.select("body")
    var svg = d3.select('#' + divName)
        .append("svg")
        .attr("width", width + margin.left + margin.right + 200)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

    var lastCircleSelected = null;

    function deselectLastCircle() {
        if (lastCircleSelected) {
            lastCircleSelected.style["stroke"] = null;
            lastCircleSelected = null;
        }
    }

    function getSentenceBoundaries(text) {
        // !!! need to use spacy's spentence splitter
        var sentenceRe = /\(?[^\.\?\!\n\b]+[\n\.!\?]\)?/g;
        var offsets = [];
        var match;
        while ((match = sentenceRe.exec(text)) != null) {
            offsets.push(match.index);
        }
        offsets.push(text.length);
        return offsets;
    }

    function getMatchingSnippet(text, boundaries, start, end) {
        var sentenceStart = null;
        var sentenceEnd = null;
        for (var i in boundaries) {
            var position = boundaries[i];
            if (position <= start && (sentenceStart == null || position > sentenceStart)) {
                sentenceStart = position;
            }
            if (position >= end) {
                sentenceEnd = position;
                break;
            }
        }
        var snippet = (text.slice(sentenceStart, start) + "<b>" + text.slice(start, end)
        + "</b>" + text.slice(end, sentenceEnd)).trim();
        return {'snippet': snippet, 'sentenceStart': sentenceStart};
    }

    function gatherTermContexts(d) {
        var category_name = fullData['info']['category_name'];
        var not_category_name = fullData['info']['not_category_name'];
        var matches = [[], []];
        if (fullData.docs === undefined) return matches;
        for (var i in fullData.docs.texts) {
            var text = fullData.docs.texts[i];
            var pattern = new RegExp("\\b(" + d.term.replace(" ", "[^\\w]+") + ")\\b", "gim");
            var match;
            var sentenceOffsets = null;
            var lastSentenceStart = null;
            if (max_snippets != null
                && matches[fullData.docs.labels[0]] >= max_snippets
                && matches[fullData.docs.labels[1]] >= max_snippets) {
                break;
            }
            while ((match = pattern.exec(text)) != null) {
                if (sentenceOffsets == null) {
                    sentenceOffsets = getSentenceBoundaries(text);
                }
                var foundSnippet = getMatchingSnippet(text, sentenceOffsets,
                    match.index, pattern.lastIndex);
                if (foundSnippet.sentenceStart == lastSentenceStart) continue;
                lastSentenceStart = foundSnippet.sentenceStart;
                var categoryMatches = matches[fullData.docs.labels[i]];
                if (max_snippets != null && categoryMatches.length >= max_snippets) {
                    break;
                }
                categoryMatches.push({
                    'snippet': foundSnippet.snippet,
                    'id': i
                });
            }
        }
        return matches;
    }

    function displayTermContexts(contexts) {
        if (contexts[0].length == 0 && contexts[1].length == 0) {
            return null;
        }
        var categoryNames = [fullData.info.category_name, fullData.info.not_category_name];
        d3.select('#cathead').html(categoryNames[0]);
        d3.select('#notcathead').html(categoryNames[1]);
        categoryNames
            .map(
                function (catName, catIndex) {
                    var divId = catIndex == 0 ? '#cat' : '#notcat';
                    var temp = d3.select(divId)
                        .selectAll("div").remove();
                    d3.select(divId)
                        .selectAll("div")
                        .data(contexts[catIndex])
                        .enter()
                        .append("div")
                        .attr('class', 'snippet')
                        .html(function (x) {
                            return x.snippet;
                        });
                });
        if (window.location.hash == '#snippets') {
            window.location.hash = '#snippetsalt';
        } else {
            window.location.hash = '#snippets';
        }
    }

    function showTooltip(d, pageX, pageY) {
        deselectLastCircle();
        tooltip.transition()
            .duration(0)
            .style("opacity", 1)
            .style("z-index", 10000000);

        tooltip.html(d.term + "<br/>" + d.cat25k + ":" + d.ncat25k + " per 25k words")
            .style("left", (pageX) + "px")
            .style("top", (pageY - 28) + "px");

        tooltip.on('click', function () {
            tooltip.transition()
                .style('opacity', 0)
        });
    }

    handleSearch = function (event) {
        deselectLastCircle();
        var searchTerm = document
            .getElementById("searchTerm")
            .value
            .toLowerCase()
            .replace("'", " '")
            .trim();
        showToolTipForTerm(searchTerm);
        displayTermContexts(gatherTermContexts(searchTermInfo));
        return false;
    };

    function showToolTipForTerm(searchTerm) {
        var searchTermInfo = termDict[searchTerm];
        if (searchTermInfo === undefined) {
            d3.select("#alertMessage")
                .text(searchTerm + " didn't make it into the visualization.");
        } else {
            d3.select("#alertMessage").text("");
            var circle = mysvg._groups[0][searchTermInfo.i];
            var mySVGMatrix = circle.getScreenCTM()
                .translate(circle.cx.baseVal.value, circle.cy.baseVal.value);
            var pageX = mySVGMatrix.e;
            var pageY = mySVGMatrix.f;
            circle.style["stroke"] = "black";
            showTooltip(searchTermInfo, pageX, pageY);
            lastCircleSelected = circle;

        }
    };

    function processData(fullData) {
        var modelInfo = fullData['info'];
        /*
         categoryTermList.data(modelInfo['category_terms'])
         .enter()
         .append("li")
         .text(function(d) {return d;});
         */
        data = fullData['data'];
        termDict = Object();
        data.forEach(function (x, i) {
            termDict[x.term] = x;
            termDict[x.term].i = i;
        });

        console.log(data);
        // Scale the range of the data.  Add some space on either end.
        x.domain([-0.1, d3.max(data, function (d) {
            return d.x;
        }) + 0.1]);
        y.domain([-0.1, d3.max(data, function (d) {
            return d.y;
        }) + 0.1]);


        var rangeTree = null; // keep boxes of all points and labels here
        // Add the scatterplot
        mysvg = svg.selectAll("dot")
            .data(data)
            .enter()
            .append("circle")
            .attr("r", 2)
            .attr("cx", function (d) {
                return x(d.x);
            })
            .attr("cy", function (d) {
                return y(d.y);
            })
            .style("fill", function (d) {
                return color(d.s);
            })
            .on("mouseover", function (d) {
                showTooltip(d, d3.event.pageX, d3.event.pageY);
                d3.select(this).style("stroke", "black");
            })
            .on("click", function (d) {
                displayTermContexts(gatherTermContexts(d));
            })
            .on("mouseout", function (d) {
                tooltip.transition()
                    .duration(0)
                    .style("opacity", 0);
                d3.select(this).style("stroke", null);
            });

        coords = Object();
        function censorPoints(datum) {
            var term = datum.term;
            //var curLabel = d3.select("body").append("div")
            var curLabel = d3.select('#' + divName).append("div")

                .attr("class", "label").html('L')
                .style("left", x(datum.x) + margin.left + 5 + 'px')
                .style("top", y(datum.y) + margin.top + 4 + 'px');
            var curDiv = curLabel._groups[0][0];

            var x1 = curDiv.offsetLeft - 2 + 2;
            var y1 = curDiv.offsetTop - 2 + 5;
            var x2 = curDiv.offsetLeft + 2 + 2;
            var y2 = curDiv.offsetTop + 2 + 5;
            /*
             var x1 = curDiv.offsetLeft - 2;
             var y1 = curDiv.offsetTop - 2;
             var x2 = curDiv.offsetLeft + 2;
             var y2 = curDiv.offsetTop + 2;
             */
            curLabel.remove();
            //if (!searchRangeTree(rangeTree, x1, y1, x2, y2)) {
            rangeTree = insertRangeTree(rangeTree, x1, y1, x2, y2, '~~' + term);
            //}
            /*
             if (term == 'an economy') {
             console.log("~~an economy " + " X" + x1 + ":" + x2 + " Y" + y1 + ":" + y2)
             }*/
            coords['~~' + term] = [x1, y1, x2, y2];
        }

        function labelPointBottomLeft(i) {
            var term = data[i].term;
            //var curLabel = d3.select("body").append("div")
            var curLabel = d3.select("#" + divName).append("div")
                .attr("class", "label").html(term)
                .style("left", x(data[i].x) + margin.left + 10 + 'px')
                .style("top", y(data[i].y) + margin.top + 8 + 'px');
            var curDiv = curLabel._groups[0][0];

            var x1 = curDiv.offsetLeft;
            var y1 = curDiv.offsetTop;
            var x2 = curDiv.offsetLeft + curDiv.offsetWidth;
            var y2 = curDiv.offsetTop + curDiv.offsetHeight;


            //move it to top right
            /*
             var width = curDiv.offsetWidth;
             var height = curDiv.offsetHeight;

             curLabel.remove();
             var curLabel = d3.select("body").append("div")
             .attr("class", "label").html(term)
             .style("left", x(data[i].x) + margin.left  + 10 - width + 'px')
             .style("top", y(data[i].y) + margin.top + 8  - height + 'px');
             var curDiv = curLabel._groups[0][0];

             var x2 = curDiv.offsetLeft;
             var y2 = curDiv.offsetTop;
             var x1 = curDiv.offsetLeft - curDiv.offsetWidth;
             var y1 = curDiv.offsetTop - curDiv.offsetHeight;
             */
            //console.log('x' + x(data[i].x) + margin.left + ' vs ' + curDiv.offsetLeft);
            //console.log(curDiv.offsetLeft - (10 + x(data[i].x) + margin.left));
            //console.log('y' + y(data[i].y) +  margin.top);
            //console.log(curDiv.offsetTop - (8 + y(data[i].y) +  margin.top));
            var matchedElement = searchRangeTree(rangeTree, x1, y1, x2, y2);
            /*
             if (term == 'affordable') {
             console.log(term + " " + " X" + x1 + ":" + x2 + " Y" + y1 + ":" + y2)
             var matchedCoord = coords[matchedElement];
             var mx1 = matchedElement[0];
             var my1 = matchedElement[1];
             var mx2 = matchedElement[2];
             var my2 = matchedElement[3];
             var x_diff = 0;
             var y_diff = 0;
             if (x1 >= mx1 && x1 < mx2) {
             x_diff = mx2 - x1;
             }
             if (x2 > mx1 && x2 <= mx2) {
             x_diff = mx1 - x2;
             }
             x1 += x_diff;
             x2 += x_diff;
             if (y1 >= my1 && y1 < my2) {
             y_diff = my2 - y1;
             }
             if (y2 > my1 && y2 <= my2) {
             y_diff = my1 - y2;
             }
             y1 += y_diff;
             y2 += y_diff;
             console.log(y_diff, x_diff)
             var matchedElement = searchRangeTree(rangeTree, x1, y1, x2, y2);
             console.log(term + " " + " X" + x1 + ":" + x2 + " Y" + y1 + ":" + y2)
             console.log('matchedElement ' + matchedElement)
             console.log('matchedElement ' + matchedCoord)

             }*/

            if (!matchedElement) { // | term == 'affordable'
                coords[term] = [x1, y1, x2, y2];
                rangeTree = insertRangeTree(rangeTree, x1, y1, x2, y2, term);
                return true;
            } else {
                curLabel.remove();
                return false;
            }

        }

        var radius = 2;
        //console.log('Data length ' + data.length);
        // prevent intersections with points.. not quite working
        /*
         for (var i = 0; i < data.length; i++) {

         //if (!searchRangeTree(rangeTree, x1, y1, x2, y2)) {
         //    rangeTree = insertRangeTree(rangeTree, x1, y1, x2, y2, i);
         //}
         }*/

        //var nodes = Array.prototype.slice.call(svg.selectAll('circle')._groups[0],0);
        //console.log("NODES");console.log(nodes);

        /*
         var nodeI = 0;
         nodes.forEach(
         function (node) {
         var rect = node.getBoundingClientRect();
         rangeTree = insertRangeTree(rangeTree, rect.left, rect.top, rect.right, rect.bottom, nodeI++);
         }
         );*/
        //console.log("Range Tree");
        //console.log(rangeTree);

        function euclideanDistanceSort(a, b) {
            var aCatDist = a.x * a.x + (1 - a.y) * (1 - a.y);
            var aNotCatDist = a.y * a.y + (1 - a.x) * (1 - a.x);
            var bCatDist = b.x * b.x + (1 - b.y) * (1 - b.y);
            var bNotCatDist = b.y * b.y + (1 - b.x) * (1 - b.x);
            return (Math.min(aCatDist, aNotCatDist) > Math.min(bCatDist, bNotCatDist)) * 2 - 1;
        }

        function euclideanDistanceSortForCategory(a, b) {
            var aCatDist = a.x * a.x + (1 - a.y) * (1 - a.y);
            var bCatDist = b.x * b.x + (1 - b.y) * (1 - b.y);
            return (aCatDist > bCatDist) * 2 - 1;
        }

        function euclideanDistanceSortForNotCategory(a, b) {
            var aNotCatDist = a.y * a.y + (1 - a.x) * (1 - a.x);
            var bNotCatDist = b.y * b.y + (1 - b.x) * (1 - b.x);
            return (aNotCatDist > bNotCatDist) * 2 - 1;
        }

        data = data.sort(euclideanDistanceSort);

        data.forEach(censorPoints);
        for (i = 0; i < data.length; labelPointBottomLeft(i++));
        //console.log("coords")
        //console.log(coords)
        // Add the X Axis
        var myXAxis = svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        var xLabel = svg.append("text")
            .attr("class", "x label")
            .attr("text-anchor", "end")
            .attr("x", width)
            .attr("y", height - 6)
            .text(modelInfo['not_category_name'] + " Frequency");
        //console.log('xLabel');
        //console.log(xLabel);

        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "30px")
            .attr("dy", "-13px")
            .attr("transform", "rotate(-90)");

        svg.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", 6)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text(modelInfo['category_name'] + " Frequency");

        word = svg.append("text")
            .attr("class", "category_header")
            .attr("text-anchor", "start")
            .attr("x", width)
            .attr("dy", "6px")
            .text("Top " + fullData['info']['category_name'] + ' Terms');

        function showWordList(word, termDataList) {
            for (var i in termDataList) {
                var curTerm = termDataList[i].term;
                word = (function (word, curTerm) {
                    return svg.append("text")
                        .attr("text-anchor", "start")
                        .attr("x", width + 10)
                        .attr("y", word.node().getBBox().y + 2 * word.node().getBBox().height)
                        .text(curTerm)
                        .on("mouseover", function (d) {
                            showToolTipForTerm(curTerm);
                            d3.select(this).style("stroke", "black");
                        })
                        .on("mouseout", function (d) {
                            tooltip.transition()
                                .duration(0)
                                .style("opacity", 0);
                            d3.select(this).style("stroke", null);
                        })
                        .on("click", function (d) {
                            displayTermContexts(gatherTermContexts(termDict[curTerm]));
                        });
                })(word, curTerm);
            }
            return word;
        }

        word = showWordList(word, data.sort(euclideanDistanceSortForCategory).slice(0, 14));

        word = svg.append("text")
            .attr("class", "category_header")
            .attr("text-anchor", "start")
            .attr("x", width)
            .attr("y", word.node().getBBox().y + 4 * word.node().getBBox().height)
            .text("Top " + fullData['info']['not_category_name'] + ' Terms');

        word = showWordList(word, data.sort(euclideanDistanceSortForNotCategory).slice(0, 14));

    };

    fullData = getDataAndInfo();
    processData(fullData);

    // The tool tip is down here in order to make sure it has the highest z-index
    var tooltip = d3.select('#' + divName)
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
}
