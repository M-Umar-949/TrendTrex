// Define data inline
const data = {
    products: ["rice", "bread", "milk", "salt", "pasta", "juice", "vegetables", "water", "coffee"],
    prices: [2.5, 1.8, 3.2, 0.5, 1.2, 1.5, 1.8, 1.0, 3.5],
    sold: [100, 80, 120, 50, 70, 90, 85, 150, 60]
};

const margin = { top: 10, right: 30, bottom: 50, left: 40 };
const width = 600 - margin.left - margin.right;
const height = 400 - margin.top - margin.bottom;

// Create SVG element
const svg = d3.select('#chart-container')
    .append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

// Define scales
const xScale = d3.scaleBand()
    .domain(data.products)
    .range([0, width])
    .padding(0.1);

const yScale = d3.scaleLinear()
    .domain([0, d3.max(data.sold)])
    .range([height, 0]);


// Draw bars
svg.selectAll('.bar')
    .data(data.products)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', d => xScale(d))
    .attr('y', d => yScale(data.sold[data.products.indexOf(d)]))
    .attr('width', xScale.bandwidth())
    .attr('height', d => height - yScale(data.sold[data.products.indexOf(d)]))
    .attr('fill', 'aliceblue')
    .on('mouseover', function() {
        d3.select(this).attr('fill', 'steelblue'); // Change color on mouseover
    })
    .on('mouseout', function() {
        d3.select(this).attr('fill', 'aliceblue'); // Revert to original color on mouseout
    });

// Add x-axis
svg.append('g')
    .attr('class', 'axis')
    .attr('transform', `translate(0, ${height})`)
    .call(d3.axisBottom(xScale))
    .attr('fill','aliceblue');

// Add y-axis
svg.append('g')
    .attr('class', 'axis')
    .call(d3.axisLeft(yScale))
    .attr('fill','aliceblue');

// Add chart title
svg.append('text')
    .attr('x', width / 2)
    .attr('y', -margin.top / 2+10)
    .attr('text-anchor', 'middle')
    .text('Product Sales')
    .attr('fill','aliceblue');


// Add x-axis label
svg.append('text')
    .attr('x', width / 2 -10)
    .attr('y', height + margin.bottom / 2 +10)
    .attr('text-anchor', 'middle')
    .text('Products')
    .attr('fill','aliceblue');

// Add y-axis label
svg.append('text')
    .attr('transform', 'rotate(-90)')
    .attr('x', -height / 2)
    .attr('y', -margin.left / 2 -10)
    .attr('text-anchor', 'middle')
    .text('Units Sold')
    .attr('fill','aliceblue');
