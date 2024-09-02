import React, { useEffect, useState } from 'react';
import './App.css';

interface Cell {
  Value: string;
  Attributes?: { Id: string; Value: string }[];
}

interface Row {
  Cells?: Cell[];
  RowType: string;
  Title?: string;
  Rows?: Row[];
}

interface Report {
  ReportDate: string;
  ReportName: string;
  ReportTitles: string[];
  Rows: Row[];
}

interface ApiResponse {
  Reports: Report[];
}

const App: React.FC = () => {
  const [report, setReport] = useState<Report | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/data.json')
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch data.json');
        }
        return response.json();
      })
      .then((data: ApiResponse) => {
        console.log('API Response:', data);
        if (data.Reports && data.Reports.length > 0) {
          setReport(data.Reports[0]);
        } else {
          setError('No report data found');
        }
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setError(error.message);
      });
  }, []);

  if (error) {
    return <div className="error">Error: {error}</div>;
  }

  if (!report) {
    return <div className="loading">Loading...</div>;
  }

  // Function to recursively render rows
  const renderRows = (rows: Row[]) => {
    return rows.map((row, rowIndex) => {
      if (row.RowType === 'Section') {
        return (
          <React.Fragment key={rowIndex}>
            <tr className="section-title">
              <td colSpan={3}>{row.Title}</td>
            </tr>
            {row.Rows && renderRows(row.Rows)}
          </React.Fragment>
        );
      } else if (row.RowType === 'Row' || row.RowType === 'SummaryRow') {
        return (
          <tr key={rowIndex} className={row.RowType === 'SummaryRow' ? 'summary-row' : ''}>
            {row.Cells?.map((cell, cellIndex) => (
              <td key={cellIndex}>{cell.Value}</td>
            ))}
          </tr>
        );
      } else if (row.RowType === 'Header') {
        return (
          <tr key={rowIndex}>
            {row.Cells?.map((cell, cellIndex) => (
              <th key={cellIndex}>{cell.Value}</th>
            ))}
          </tr>
        );
      }
      return null;
    });
  };

  return (
    <div className="App">
      <h1>{report.ReportName}</h1>
      <h2>As at {report.ReportDate}</h2>
      <table>
        <thead>
          {renderRows(report.Rows.filter(row => row.RowType === 'Header'))}
        </thead>
        <tbody>
          {renderRows(report.Rows.filter(row => row.RowType !== 'Header'))}
        </tbody>
      </table>
    </div>
  );
};

export default App;