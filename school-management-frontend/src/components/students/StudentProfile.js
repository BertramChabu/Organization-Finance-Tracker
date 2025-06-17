import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, Container, Tab, Tabs, Spinner, Alert, Table, Badge } from 'react-bootstrap';
import API from '../../services/api';

const StudentProfile = () => {
  const { id } = useParams();
  const [student, setStudent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    const fetchStudent = async () => {
      try {
        const response = await API.get(`students/${id}/`);
        setStudent(response.data);
      } catch (err) {
        setError(err.message || 'Failed to fetch student data');
      } finally {
        setLoading(false);
      }
    };
    fetchStudent();
  }, [id]);

  if (loading) return <Spinner animation="border" className="d-block mx-auto mt-5" />;
  if (error) return <Alert variant="danger" className="mt-4">{error}</Alert>;
  if (!student) return null;

  return (
    <Container className="mt-4">
      <Card className="shadow">
        <Card.Body>
          <div className="d-flex align-items-center mb-4">
            <div className="me-4">
              <div 
                className="rounded-circle bg-secondary d-flex align-items-center justify-content-center" 
                style={{ width: '100px', height: '100px' }}
              >
                <span className="text-white fs-3">
                  {student.user.first_name.charAt(0)}{student.user.last_name.charAt(0)}
                </span>
              </div>
            </div>
            <div>
              <h2>{student.user.first_name} {student.user.last_name}</h2>
              <div className="d-flex gap-3">
                <span><strong>Admission No:</strong> {student.admission_number}</span>
                <span><strong>Class:</strong> {student.current_class?.name || 'N/A'}</span>
                <Badge bg={student.is_active ? 'success' : 'secondary'}>
                  {student.is_active ? 'Active' : 'Inactive'}
                </Badge>
              </div>
            </div>
          </div>

          <Tabs
            activeKey={activeTab}
            onSelect={(k) => setActiveTab(k)}
            className="mb-4"
          >
            <Tab eventKey="profile" title="Profile">
              <div className="mt-4">
                <Table striped bordered>
                  <tbody>
                    <tr>
                      <td><strong>Gender</strong></td>
                      <td>{student.gender === 'M' ? 'Male' : 'Female'}</td>
                    </tr>
                    <tr>
                      <td><strong>Date of Admission</strong></td>
                      <td>{new Date(student.date_of_admission).toLocaleDateString()}</td>
                    </tr>
                    <tr>
                      <td><strong>KCPE Marks</strong></td>
                      <td>{student.kcpe_marks || 'N/A'}</td>
                    </tr>
                    <tr>
                      <td><strong>Email</strong></td>
                      <td>{student.user.email}</td>
                    </tr>
                    <tr>
                      <td><strong>Username</strong></td>
                      <td>{student.user.username}</td>
                    </tr>
                  </tbody>
                </Table>
              </div>
            </Tab>
            <Tab eventKey="performance" title="Performance">
              <div className="mt-4">
                <h5>Academic Performance</h5>
                <p>Performance data will be displayed here</p>
              </div>
            </Tab>
            <Tab eventKey="attendance" title="Attendance">
              <div className="mt-4">
                <h5>Attendance Records</h5>
                <p>Attendance data will be displayed here</p>
              </div>
            </Tab>
          </Tabs>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default StudentProfile;