import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Form, Button, Container, Alert, Spinner, Card, Row, Col } from 'react-bootstrap';
import API from '../../services/api';

const ExamForm = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [academicYears, setAcademicYears] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    exam_type: 'cat',
    academic_year: '',
    start_date: new Date().toISOString().split('T')[0],
    end_date: new Date().toISOString().split('T')[0],
    is_published: false
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [yearsRes] = await Promise.all([
          API.get('academic-years/')
        ]);
        setAcademicYears(yearsRes.data);

        if (id) {
          const examRes = await API.get(`exams/${id}/`);
          setFormData(examRes.data);
        }
      } catch (err) {
        setError(err.message || 'Failed to fetch data');
      }
    };
    fetchData();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      if (id) {
        await API.put(`exams/${id}/`, formData);
      } else {
        await API.post('exams/', formData);
      }
      navigate('/exams');
    } catch (err) {
      setError(err.response?.data || err.message || 'Operation failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="mt-4">
      <Card className="shadow">
        <Card.Body>
          <h2 className="mb-4">{id ? 'Edit' : 'Add'} Exam</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          
          <Form onSubmit={handleSubmit}>
            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Exam Name</Form.Label>
                  <Form.Control
                    type="text"
                    value={formData.name}
                    onChange={(e) => setFormData({
                      ...formData,
                      name: e.target.value
                    })}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Exam Type</Form.Label>
                  <Form.Select
                    value={formData.exam_type}
                    onChange={(e) => setFormData({
                      ...formData,
                      exam_type: e.target.value
                    })}
                    required
                  >
                    <option value="cat">CAT</option>
                    <option value="midterm">Mid-Term</option>
                    <option value="endterm">End-Term</option>
                    <option value="mock">Mock Exam</option>
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Academic Year</Form.Label>
                  <Form.Select
                    value={formData.academic_year}
                    onChange={(e) => setFormData({
                      ...formData,
                      academic_year: e.target.value
                    })}
                    required
                  >
                    <option value="">Select Academic Year</option>
                    {academicYears.map(year => (
                      <option key={year.id} value={year.id}>
                        {year.year}
                      </option>
                    ))}
                  </Form.Select>
                </Form.Group>
              </Col>
            </Row>

            <Row>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>Start Date</Form.Label>
                  <Form.Control
                    type="date"
                    value={formData.start_date}
                    onChange={(e) => setFormData({
                      ...formData,
                      start_date: e.target.value
                    })}
                    required
                  />
                </Form.Group>
              </Col>
              <Col md={6}>
                <Form.Group className="mb-3">
                  <Form.Label>End Date</Form.Label>
                  <Form.Control
                    type="date"
                    value={formData.end_date}
                    onChange={(e) => setFormData({
                      ...formData,
                      end_date: e.target.value
                    })}
                    required
                  />
                </Form.Group>
              </Col>
            </Row>

            <Form.Check
              type="switch"
              id="publish-switch"
              label="Publish Exam"
              checked={formData.is_published}
              onChange={(e) => setFormData({
                ...formData,
                is_published: e.target.checked
              })}
            />

            <div className="mt-4">
              <Button variant="primary" type="submit" disabled={loading}>
                {loading ? <Spinner size="sm" /> : 'Save Exam'}
              </Button>{' '}
              <Button variant="secondary" onClick={() => navigate('/exams')}>
                Cancel
              </Button>
            </div>
          </Form>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default ExamForm;