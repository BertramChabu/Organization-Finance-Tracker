import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Table, Button, Container, Spinner, Alert, Form } from 'react-bootstrap';
import API from '../../services/api';

const ResultsEntry = ({ examId, classId }) => {
  const [students, setStudents] = useState([]);
  const [subjects, setSubjects] = useState([]);
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [studentsRes, subjectsRes, existingResultsRes] = await Promise.all([
          API.get(`classes/${classId}/students/`),
          API.get(`classes/${classId}/subjects/`),
          API.get(`exams/${examId}/results/?class_id=${classId}`)
        ]);
        
        setStudents(studentsRes.data);
        setSubjects(subjectsRes.data);
        
        // Initialize results with existing data if available
        const initialResults = {};
        studentsRes.data.forEach(student => {
          initialResults[student.id] = {};
          subjectsRes.data.forEach(subject => {
            const existingResult = existingResultsRes.data.find(
              r => r.student.id === student.id && r.subject.id === subject.id
            );
            initialResults[student.id][subject.id] = existingResult?.marks || '';
          });
        });
        setResults(initialResults);
      } catch (err) {
        setError(err.message || 'Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [examId, classId]);

  const handleResultChange = (studentId, subjectId, value) => {
    setResults(prev => ({
      ...prev,
      [studentId]: {
        ...prev[studentId],
        [subjectId]: value
      }
    }));
  };

  const submitResults = async () => {
    setSaving(true);
    try {
      const resultsToSubmit = [];
      Object.keys(results).forEach(studentId => {
        Object.keys(results[studentId]).forEach(subjectId => {
          if (results[studentId][subjectId]) {
            resultsToSubmit.push({
              exam: examId,
              student: studentId,
              subject: subjectId,
              marks: parseFloat(results[studentId][subjectId])
            });
          }
        });
      });
      
      await API.post('exam-results/bulk/', resultsToSubmit);
      setError(null);
      setSaving(false);
      alert('Results submitted successfully!');
    } catch (err) {
      setError(err.response?.data || err.message || 'Failed to submit results');
      setSaving(false);
    }
  };

  if (loading) return <Spinner animation="border" className="d-block mx-auto mt-5" />;
  if (error) return <Alert variant="danger" className="mt-4">{error}</Alert>;

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Enter Exam Results</h2>
      
      <div className="table-responsive">
        <Table striped bordered hover>
          <thead>
            <tr>
              <th>Student</th>
              {subjects.map(subject => (
                <th key={subject.id}>{subject.name}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {students.map(student => (
              <tr key={student.id}>
                <td>{student.user.first_name} {student.user.last_name}</td>
                {subjects.map(subject => (
                  <td key={subject.id}>
                    <Form.Control
                      type="number"
                      min="0"
                      max="100"
                      step="0.01"
                      value={results[student.id]?.[subject.id] || ''}
                      onChange={(e) => handleResultChange(student.id, subject.id, e.target.value)}
                      size="sm"
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      </div>

      <div className="d-flex justify-content-end mt-3">
        <Button 
          variant="primary" 
          onClick={submitResults}
          disabled={saving}
        >
          {saving ? 'Saving...' : 'Save All Results'}
        </Button>
      </div>
    </Container>
  );
};

export default ResultsEntry;