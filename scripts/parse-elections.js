const fs = require( "fs" );

const data = fs.readFileSync('raw-data.txt', 'utf8');

const lines = data.split('\n');

const csvLines = lines.map( line => {
  const data = line.trim().split(/\s+/);

  const percents = data.slice(4, 6).map( wholeNum => {
    return wholeNum / 100;
  });

  const clintonWin = percents[0] > percents[1] ? 1 : 0;
  percents.push(clintonWin);

  return percents.join(',');
});

console.log( csvLines[0] );

csvLines.unshift('Clinton,Trump,ClintonWin');

const csv = csvLines.join('\n');

fs.writeFileSync('election-data.csv', csv, 'utf8');
