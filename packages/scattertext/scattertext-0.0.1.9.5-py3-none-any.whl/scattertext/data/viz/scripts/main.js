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
            if(fullData.docs.labels[i] > 1) continue;
            var text = fullData.docs.texts[i];
            var pattern = new RegExp("\\b(" + d.term.replace(" ", "[^\\w]+") + ")\\b", "gim");
            var match;
            var sentenceOffsets = null;
            var lastSentenceStart = null;
            while ((match = pattern.exec(text)) != null) {
                if (sentenceOffsets == null) {
                    sentenceOffsets = getSentenceBoundaries(text);
                }
                var foundSnippet = getMatchingSnippet(text, sentenceOffsets,
                    match.index, pattern.lastIndex);
                if (foundSnippet.sentenceStart == lastSentenceStart) continue;
                lastSentenceStart = foundSnippet.sentenceStart;
                var categoryMatches = matches[fullData.docs.labels[i]];
                categoryMatches.push({
                    'snippet': foundSnippet.snippet,
                    'id': i
                });
            }
        }
        return {'contexts': matches, 'info': d};
    }

    function displayTermContexts(termInfo, jump=true) {
        var contexts = termInfo.contexts;
        var info = termInfo.info;
        if (contexts[0].length == 0 && contexts[1].length == 0) {
            return null;
        }
        var categoryNames = [fullData.info.category_name,
            fullData.info.not_category_name];
        d3.select('#cathead').html(categoryNames[0]);
        d3.select('#notcathead').html(categoryNames[1]);
        categoryNames
            .map(
                function (catName, catIndex) {
                    if (max_snippets != null) {
                        var contextsToDisplay = contexts[catIndex].slice(0, max_snippets);
                    }
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
        d3.select('#termstats')
            .selectAll("div")
            .remove();
        d3.select('#termstats')
            .append('div')
            .attr("class", "snippet_header")
            .html('Term: <b>' + info.term + '</b>');
        d3.select('#termstats')
            .append('div')
            .attr("class", "text_subheader")
            .html('<table align="center" cellpadding="3"><tr><td rowspan="2">Usage per 25,000 words</td><td>'
                + fullData.info.category_name + ': ' + info.cat25k + '</td></tr><tr><td>' +
                fullData.info.not_category_name + ': ' + info.ncat25k + '</td></tr></table>');
        console.log(info);
        if (jump) {
            if (window.location.hash == '#snippets') {
                window.location.hash = '#snippetsalt';
            } else {
                window.location.hash = '#snippets';
            }
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
        displayTermContexts(gatherTermContexts(termDict[searchTerm]), false);
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

    function makeWordInteractive(domObj, term) {
        return domObj
            .on("mouseover", function (d) {
                showToolTipForTerm(term);
                d3.select(this).style("stroke", "black");
            })
            .on("mouseout", function (d) {
                tooltip.transition()
                    .duration(0)
                    .style("opacity", 0);
                d3.select(this).style("stroke", null);
            })
            .on("click", function (d) {
                displayTermContexts(gatherTermContexts(termDict[term]));
            });
    }

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
            var curLabel = svg.append("text")
                .attr("x", x(datum.x))
                .attr("y", y(datum.y) + 3)
                .attr("text-anchor", "middle")
                .text("x");
            var bbox = curLabel.node().getBBox();
            var borderToRemove = .5;
            var x1 = bbox.x + borderToRemove,
                y1 = bbox.y + borderToRemove,
                x2 = bbox.x + bbox.width - borderToRemove,
                y2 = bbox.y + bbox.height - borderToRemove;
            rangeTree = insertRangeTree(rangeTree, x1, y1, x2, y2, '~~' + term);
            curLabel.remove();
        }

        function labelPointBottomLeft(i) {
            var term = data[i].term;

            var configs = [
                {'anchor': 'end', 'xoff': -5, 'yoff': -3},
                //{'anchor': 'end', 'xoff': -5, 'yoff': 10},
                {'anchor': 'start', 'xoff': 3, 'yoff': 10}
                //{'anchor': 'start', 'xoff': 3, 'yoff': -3}
            ];
            var matchedElement = null;
            for (var configI in configs) {
                var config = configs[configI];
                var curLabel = makeWordInteractive(
                    svg.append("text")
                        .attr("x", x(data[i].x) + config['xoff'])
                        .attr("y", y(data[i].y) + config['yoff'])
                        .attr('class', 'label')
                        .attr("text-anchor", config['anchor'])
                        .text(term),
                    term
                );
                var bbox = curLabel.node().getBBox();
                var borderToRemove = .5;
                var x1 = bbox.x + borderToRemove,
                    y1 = bbox.y + borderToRemove,
                    x2 = bbox.x + bbox.width - borderToRemove,
                    y2 = bbox.y + bbox.height - borderToRemove;
                matchedElement = searchRangeTree(rangeTree, x1, y1, x2, y2);
                if (matchedElement) {
                    curLabel.remove();
                } else {
                    break;
                }
            }

            if (!matchedElement || term == 'auto') {
                coords[term] = [x1, y1, x2, y2];
                rangeTree = insertRangeTree(rangeTree, x1, y1, x2, y2, term);
                return true;

            } else {
                //curLabel.remove();
                return false;
            }

        }

        var radius = 2;

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

        var myXAxis = svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        function registerFigureBBox(curLabel) {
            var bbox = curLabel.node().getBBox();
            var borderToRemove = 1.5;
            var x1 = bbox.x + borderToRemove,
                y1 = bbox.y + borderToRemove,
                x2 = bbox.x + bbox.width - borderToRemove,
                y2 = bbox.y + bbox.height - borderToRemove;
            return insertRangeTree(rangeTree, x1, y1, x2, y2, '~~_other_');
        }

        //rangeTree = registerFigureBBox(myXAxis);


        var xLabel = svg.append("text")
            .attr("class", "x label")
            .attr("text-anchor", "end")
            .attr("x", width)
            .attr("y", height - 6)
            .text(modelInfo['not_category_name'] + " Frequency");
        //console.log('xLabel');
        //console.log(xLabel);

        //rangeTree = registerFigureBBox(xLabel);
        // Add the Y Axis
        var myYAxis = svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dx", "30px")
            .attr("dy", "-13px")
            .attr("transform", "rotate(-90)");
        rangeTree = registerFigureBBox(myYAxis);

        var yLabel = svg.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", 6)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text(modelInfo['category_name'] + " Frequency");
        //rangeTree = registerFigureBBox(yLabel);

        word = svg.append("text")
            .attr("class", "category_header")
            .attr("text-anchor", "start")
            .attr("x", width)
            .attr("dy", "6px")
            .text("Top " + fullData['info']['category_name'] + ' Terms');
        //rangeTree = registerFigureBBox(word);

        function showWordList(word, termDataList) {
            for (var i in termDataList) {
                var curTerm = termDataList[i].term;
                word = (function (word, curTerm) {
                    return makeWordInteractive(
                        svg.append("text")
                            .attr("text-anchor", "start")
                            .attr("x", width + 10)
                            .attr("y", word.node().getBBox().y
                                + 2 * word.node().getBBox().height)
                            .text(curTerm)
                        ,
                        curTerm);
                })(word, curTerm);
                rangeTree = registerFigureBBox(word);
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

        for (i = 0; i < data.length; labelPointBottomLeft(i++));


    };

    fullData = getDataAndInfo();
    processData(fullData);

    // The tool tip is down here in order to make sure it has the highest z-index
    var tooltip = d3.select('#' + divName)
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);
}
