import React, { useState, useEffect } from 'react';
import { Table, Button, Container, Spinner, Alert, Form, Row, Col } from 'react-bootstrap';
import API from '../../services/api';

const StudentList = ({ schoolId }) => {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        const response = await API.get(`schools/${schoolId}/students/`);
        setStudents(response.data);
      } catch (err) {
        setError(err.message || 'Failed to fetch students');
      } finally {
        setLoading(false);
      }
    };
    fetchStudents();
  }, [schoolId]);

  const filteredStudents = students.filter(student => 
    student.user.first_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.user.last_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    student.admission_number.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Container className="mt-4">
      <h2 className="mb-4">Student Management</h2>
      
      <Row className="mb-3">
        <Col md={6}>
          <Form.Group>
            <Form.Control
              type="text"
              placeholder="Search students..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </Form.Group>
        </Col>
        <Col md={6} className="text-end">
          <Button variant="success" href="/students/add">
            Add New Student
          </Button>
        </Col>
      </Row>

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
              <th>Admission No.</th>
              <th>Name</th>
              <th>Class</th>
              <th>Gender</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredStudents.map(student => (
              <tr key={student.id}>
                <td>{student.admission_number}</td>
                <td>{student.user.first_name} {student.user.last_name}</td>
                <td>{student.current_class?.name || 'N/A'}</td>
                <td>{student.gender}</td>
                <td>
                  <span className={`badge ${student.is_active ? 'bg-success' : 'bg-secondary'}`}>
                    {student.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td>
                  <Button variant="info" size="sm" href={`/students/${student.id}`}>
                    View
                  </Button>{' '}
                  <Button variant="warning" size="sm" href={`/students/${student.id}/edit`}>
                    Edit
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

export default StudentList;