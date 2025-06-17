import React, { useState, useEffect } from 'react';
import { Table, Button, Container, Spinner, Alert, Badge } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import API from '../../services/api';

const ExamList = ({ schoolId }) => {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchExams = async () => {
      try {
        const response = await API.get(`schools/${schoolId}/exams/`);
        setExams(response.data);
      } catch (err) {
        setError(err.message || 'Failed to fetch exams');
      } finally {
        setLoading(false);
      }
    };
    fetchExams();
  }, [schoolId]);

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Exam Management</h2>
      
      <div className="d-flex justify-content-end mb-3">
        <Button as={Link} to="/exams/add" variant="success">
          Add New Exam
        </Button>
      </div>

      {loading ? (
        <div className="text-center">
          <Spinner animation="border" />
        </div>
      ) : error ? (
        <Alert variant="danger">{error}</Alert>
      ) : (
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>Exam Name</th>
              <th>Type</th>
              <th>Academic Year</th>
              <th>Date Range</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {exams.map(exam => (
              <tr key={exam.id}>
                <td>{exam.name}</td>
                <td>
                  <Badge bg="info">
                    {exam.exam_type.toUpperCase()}
                  </Badge>
                </td>
                <td>{exam.academic_year.year}</td>
                <td>
                  {new Date(exam.start_date).toLocaleDateString()} - {' '}
                  {new Date(exam.end_date).toLocaleDateString()}
                </td>
                <td>
                  <Badge bg={exam.is_published ? 'success' : 'warning'}>
                    {exam.is_published ? 'Published' : 'Draft'}
                  </Badge>
                </td>
                <td>
                  <Button 
                    as={Link}
                    to={`/exams/${exam.id}`}
                    variant="info" 
                    size="sm"
                  >
                    View
                  </Button>{' '}
                  <Button 
                    as={Link}
                    to={`/exams/${exam.id}/results`}
                    variant="primary" 
                    size="sm"
                  >
                    Enter Results
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  );
};

export default ExamList;