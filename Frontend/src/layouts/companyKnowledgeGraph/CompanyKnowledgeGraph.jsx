import * as d3 from 'd3';
import React, { useEffect, useRef, useState, useCallback } from 'react';

// Main React App component
const CompanyKnowledgeGraph = ({ data }) => {
    // useRef to get a direct reference to the SVG DOM element
    const svgRef = useRef(null);
    // useState for managing the tooltip's state (visibility, content, position)
    const [tooltip, setTooltip] = useState({
        isVisible: false,
        content: '',
        x: 0,
        y: 0,
    });

    // Static graph data
    const graphData = data;
    // const graphData = {
    //     "nodes": [
    //         {
    //             "id": "A1 Garage Door Service",
    //             "label": "A1 Garage Door Service",
    //             "type": "Company",
    //             "properties": {
    //                 "industry": "Home Services (Garage Door Repair and Installation)",
    //                 "founder": "Tommy Mello",
    //                 "current_ceo": "Tommy Mello",
    //                 "employee_count": 350,
    //                 "products_and_services": [
    //                     "Residential garage door repair",
    //                     "Residential garage door replacement",
    //                     "Garage door installation",
    //                     "24/7 emergency repairs"
    //                 ]
    //             }
    //         },
    //         {
    //             "id": "Cortec Group",
    //             "label": "Cortec Group",
    //             "type": "Company"
    //         },
    //         {
    //             "id": "A1 Garage Door Specialists, LLC.",
    //             "label": "A1 Garage Door Specialists, LLC.",
    //             "type": "Company"
    //         },
    //         {
    //             "id": "The Garage Door Guy Inc.",
    //             "label": "The Garage Door Guy Inc.",
    //             "type": "Company"
    //         },
    //         {
    //             "id": "Ideal Garage Doors",
    //             "label": "Ideal Garage Doors",
    //             "type": "Company"
    //         },
    //         {
    //             "id": "The Garage Doctor",
    //             "label": "The Garage Doctor",
    //             "type": "Company"
    //         },
    //         {
    //             "id": "American Veteran Garage Door Repair",
    //             "label": "American Veteran Garage Door Repair",
    //             "type": "Company"
    //         }
    //     ],
    //     "edges": [
    //         {
    //             "source": "Cortec Group",
    //             "target": "A1 Garage Door Service",
    //             "type": "ACQUIRED",
    //             "properties": {
    //                 "date": "Jan, 2023",
    //                 "deal_type": "Acquisition"
    //             }
    //         },
    //         {
    //             "source": "A1 Garage Door Service",
    //             "target": "A1 Garage Door Specialists, LLC.",
    //             "type": "ACQUIRED",
    //             "properties": {
    //                 "date": "Feb 07, 2023",
    //                 "deal_type": "Acquisition"
    //             }
    //         },
    //         {
    //             "source": "A1 Garage Door Service",
    //             "target": "The Garage Door Guy Inc.",
    //             "type": "ACQUIRED",
    //             "properties": {
    //                 "date": "Mar 13, 2024",
    //                 "deal_type": "Acquisition"
    //             }
    //         },
    //         {
    //             "source": "A1 Garage Door Service",
    //             "target": "Ideal Garage Doors",
    //             "type": "ACQUIRED",
    //             "properties": {
    //                 "date": "Jul 10, 2024",
    //                 "deal_type": "Acquisition"
    //             }
    //         },
    //         {
    //             "source": "A1 Garage Door Service",
    //             "target": "The Garage Doctor",
    //             "type": "ACQUIRED",
    //             "properties": {
    //                 "date": "Dec 19, 2024",
    //                 "deal_type": "Acquisition"
    //             }
    //         },
    //         {
    //             "source": "A1 Garage Door Service",
    //             "target": "American Veteran Garage Door Repair",
    //             "type": "ACQUIRED",
    //             "properties": {
    //                 "date": "Jul 23, 2024",
    //                 "deal_type": "Acquisition"
    //             }
    //         }
    //     ]
    // };

    // useCallback to memoize the D3 rendering logic
    const renderGraph = useCallback(() => {
        // Clear previous SVG content to prevent duplicates on re-render
        d3.select(svgRef.current).selectAll('*').remove();

        const svg = d3.select(svgRef.current);
        const container = d3.select(svgRef.current.parentNode);
        const width = container.node().getBoundingClientRect().width;
        const height = container.node().getBoundingClientRect().height;

        // Set SVG dimensions based on the container's responsive size
        svg.attr("width", width).attr("height", height);

        // Define fixed positions for nodes based on screen size and hierarchy
        const nodePositions = {
            [data?.nodes[0].id]: { x: width * 0.5, y: height * 0.2 },
            [data?.nodes[1].id]: { x: width * 0.2, y: height * 0.2 }
        };

        // Filter and sort acquired companies by date for chronological layout
        const acquiredCompanies = graphData.nodes.filter(d =>
            d.id !== data?.nodes[0].id && d.id !== data?.nodes[1].id
        );

        // Create a mapping of company ID to acquisition date for sorting
        const acquisitionDates = {};
        graphData.edges.forEach(edge => {
            if (edge.type === "ACQUIRED" && edge.source === data?.nodes[0].id) {
                acquisitionDates[edge.target] = new Date(edge.properties.date);
            } else if (edge.type === "ACQUIRED" && edge.target === data?.nodes[0].id) {
                acquisitionDates[edge.source] = new Date(edge.properties.date); // For Cortec acquiring A1
            }
        });

        // Sort acquired companies based on their acquisition date
        const sortedAcquiredCompanies = acquiredCompanies.sort((a, b) => {
            const dateA = acquisitionDates[a.id] || new Date('1900-01-01'); // Default early date if no acquisition date
            const dateB = acquisitionDates[b.id] || new Date('1900-01-01');
            return dateA - dateB;
        });

        // Arrange acquired companies in a horizontal line below A1
        const startX = width * 0.15;
        // Ensure spacingX handles cases with 0 or 1 acquired companies to avoid division by zero
        const spacingX = sortedAcquiredCompanies.length > 1 ? (width * 0.7) / (sortedAcquiredCompanies.length - 1) : 0;

        sortedAcquiredCompanies.forEach((company, i) => {
            nodePositions[company.id] = {
                x: startX + i * spacingX,
                y: (height * 0.5) + (i * 25)
            };
        });

        // Apply fixed positions to nodes
        graphData.nodes.forEach(d => {
            d.fx = nodePositions[d.id].x;
            d.fy = nodePositions[d.id].y;
        });

        // Define arrow markers in SVG defs
        const defs = svg.append("defs");

        defs.append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 30) // Position the arrow tip further away from the target node
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", "#9ca3af"); // Gray arrow

        defs.append("marker")
            .attr("id", "arrowhead-acquired")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 30)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", "#22c55e"); // Green arrow for acquired relationships

        // Create a force simulation (used only for initial positioning and link updates)
        const simulation = d3.forceSimulation(graphData.nodes)
            .force("link", d3.forceLink(graphData.edges).id(d => d.id).distance(120)) // Link force with distance
            .force("charge", d3.forceManyBody().strength(-0)) // No repulsion as nodes are fixed
            .force("center", d3.forceCenter(0, 0)) // Initial center, will be overridden by fixed positions
            .alphaTarget(0) // Stop simulation immediately after initial layout
            .on("tick", ticked);

        // Add link groups (containing line and text)
        const linkGroup = svg.append("g")
            .attr("class", "links")
            .selectAll(".link-group")
            .data(graphData.edges)
            .enter().append("g")
            .attr("class", d => `link-group link-group-${d.type.toLowerCase()}`);

        // Append line to each link group
        linkGroup.append("line")
            .attr("class", "link-line")
            .attr("stroke", d => d.type === "ACQUIRED" ? "#22c55e" : "#9ca3af") // Apply green for 'ACQUIRED'
            .attr("marker-end", d => d.type === "ACQUIRED" ? "url(#arrowhead-acquired)" : "url(#arrowhead)");

        // Append text label to each link group
        linkGroup.append("text")
            .attr("class", "link-label")
            .attr("text-anchor", "middle") // Center the text horizontally
            .attr("dy", -10) // Offset text slightly above the line
            .text(d => {
                if (d.properties && d.properties.deal_type && d.properties.date) {
                    return `${d.properties.deal_type}`;
                }
                return d.type; // Fallback to just type if properties are missing
            });

        // Add nodes (circles and text)
        const node = svg.append("g")
            .attr("class", "nodes")
            .selectAll(".node")
            .data(graphData.nodes)
            .enter().append("g")
            .attr("class", d => `node ${d.id === data?.nodes[0].id ? "main-node" : ""}`); // Add main-node class for special styling

        // Append circle to each node group
        node.append("circle")
            .attr("r", 25); // Node radius

        // Append text label to each node group
        node.append("text")
            .attr("dy", 40) // Adjusted dy to place text below the circle (radius 25 + offset)
            .text(d => d.label.length > 20 ? d.label.slice(0, 20) + '...' : d.label);

        // Tooltip functions for NODES
        node.on("mouseover", function(event, d) {
            let content = `<div class="tooltip-title">${d.label}</div>`;
            if (d.properties) {
                for (const key in d.properties) {
                    let value = d.properties[key];
                    if (Array.isArray(value)) {
                        value = value.join(", "); // Join array items for display
                    }
                    content += `<div class="tooltip-item"><strong>${key.charAt(0).toUpperCase() + key.replace(/_/g, ' ').slice(1)}:</strong> ${value}</div>`;
                }
            } else {
                content += `<div class="tooltip-item">No additional properties.</div>`;
            }
            // Update tooltip state
            setTooltip({
                isVisible: true,
                content: content,
                x: event.pageX + 10,
                y: event.pageY - 20,
            });
        })
        .on("mouseout", function() {
            setTooltip({ ...tooltip, isVisible: false }); // Hide tooltip
        });

        // Tooltip functions for LINKS (applied to linkGroup)
        linkGroup.on("mouseover", function(event, d) {
            let content = `<div class="tooltip-title">Relationship: ${d.type}</div>`;
            if (d.properties) {
                for (const key in d.properties) {
                    content += `<div class="tooltip-item"><strong>${key.charAt(0).toUpperCase() + key.replace(/_/g, ' ').slice(1)}:</strong> ${d.properties[key]}</div>`;
                }
            }
            // Update tooltip state
            setTooltip({
                isVisible: true,
                content: content,
                x: event.pageX + 10,
                y: event.pageY - 20,
            });
        })
        .on("mouseout", function() {
            setTooltip({ ...tooltip, isVisible: false }); // Hide tooltip
        });

        // Tick function to update positions on each simulation step
        function ticked() {
            linkGroup.select("line")
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);

            // Position link labels at the midpoint, always horizontal
            linkGroup.select("text")
                .attr("x", d => (d.source.x + d.target.x) / 2)
                .attr("y", d => (d.source.y + d.target.y) / 2);

            node
                .attr("transform", d => `translate(${d.x},${d.y})`);
        }

        // Cleanup simulation on component unmount
        return () => {
            simulation.stop();
        };
    }, [graphData, tooltip]); // Re-run effect if graphData changes (though static here) or tooltip state for re-render if needed

    // useEffect for window resize listener and initial graph render
    useEffect(() => {
        renderGraph(); // Initial render

        const handleResize = () => {
            renderGraph(); // Re-render on resize
        };

        window.addEventListener('resize', handleResize);

        // Cleanup event listener on component unmount
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, [renderGraph, data]); // Depend on renderGraph to ensure it's up-to-date

    return (
        <div>
            {/* Main graph container */}
            <div className="">
                <h1 className="">Company Relationship Graph</h1>
                {/* <div className="graph-info bg-blue-100 rounded-xl p-4 mb-6 text-center text-blue-700">
                    <p className="my-2 text-sm">Nodes are fixed and arranged chronologically. <strong className="font-bold">A1 Garage Door Service is highlighted in red.</strong></p>
                    <p className="my-2 text-sm">Hover over nodes for details, and over <strong className="font-bold">links</strong> for acquisition details. <strong className="font-bold">Arrows and labels show relationship direction and details.</strong></p>
                    <p className="my-2 text-sm">Green links indicate an 'ACQUIRED' relationship.</p>
                </div> */}
                {/* SVG container for responsive D3 graph */}
                <div style={{height: '75vh'}}>
                    <svg ref={svgRef} className=""></svg>
                </div>
                {/* Tooltip element, conditionally rendered based on state */}
                <div
                    className={`tooltip ${tooltip.isVisible ? 'active' : ''}`}
                    style={{ left: tooltip.x, top: tooltip.y }}
                    dangerouslySetInnerHTML={{ __html: tooltip.content }}
                ></div>
            </div>

            {/* Custom CSS for D3 elements and specific overrides */}
            <style>{`
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

                .node circle {
                    stroke: #3b82f6; /* Default Blue stroke */
                    stroke-width: 2px;
                    fill: #60a5fa; /* Default Lighter blue fill */
                    transition: all 0.2s ease-in-out;
                }

                /* Specific style for the main node (A1 Garage Door Service) */
                .node.main-node circle {
                    fill: #dc2626; /* Red fill */
                    stroke: #b91c1c; /* Darker red stroke */
                }

                .node circle:hover {
                    fill: #3b82f6; /* Darker blue on hover */
                    stroke: #1e3a8a;
                    transform: scale(1.1); /* Slight scale on hover */
                }

                /* Hover effect for the main node */
                .node.main-node circle:hover {
                    fill: #ef4444; /* Lighter red on hover */
                    stroke: #991b1b; /* Even darker red stroke on hover */
                }

                .node text {
                    font-size: 0.9rem; /* Slightly larger text for nodes */
                    font-weight: 600;
                    fill: #1f2937; /* Dark gray text */
                    text-anchor: middle;
					text-wrap: wrap;
                    pointer-events: none; /* Allows clicks to pass through text to shape */
                    text-shadow: 0 0 5px rgba(255, 255, 255, 0.7); /* Text shadow for readability */
                }

                .link-line { /* Renamed from .link to .link-line */
                    stroke: #9ca3af; /* Gray link color */
                    stroke-opacity: 0.6;
                    stroke-width: 2px;
                }

                .link-group:hover .link-line { /* Apply hover styles to the line within the group */
                    stroke-width: 4px; /* Thicker on hover */
                    stroke-opacity: 1; /* More opaque on hover */
                }

                .link-group {
                    cursor: help; /* Indicate hoverable link for the entire group */
                    transition: all 0.2s ease-in-out; /* Transition for the group */
                }

                .link-label {
                    font-size: 0.75rem; /* Smaller text for clarity */
                    fill: #374151; /* Darker gray for readability */
                    pointer-events: none; /* Crucial so it doesn't block link hover */
                    text-shadow: 0 0 3px rgba(255, 255, 255, 0.8); /* For contrast */
                }

                /* Tooltip for node details */
                .tooltip {
                    position: absolute;
                    background-color: #333;
                    color: #fff;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-size: 0.85rem;
                    pointer-events: none; /* So it doesn't interfere with mouse events on the graph */
                    opacity: 0;
                    transition: opacity 0.2s ease-in-out;
                    max-width: 250px;
                    z-index: 10;
                }

                .tooltip.active {
                    opacity: 0.9;
                }

                .tooltip-title {
                    font-weight: bold;
                    margin-bottom: 5px;
                    color: #60a5fa;
                }

                .tooltip-item {
                    margin-bottom: 3px;
                }
            `}</style>
        </div>
    );
}

export default CompanyKnowledgeGraph;