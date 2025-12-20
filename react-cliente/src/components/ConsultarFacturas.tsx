import React, { useState } from 'react';
import { 
  Form, 
  Button, 
  Row, 
  Col, 
  Card, 
  Alert, 
  Spinner,
  FormControl,
  FormGroup,
  FormLabel,
  FormSelect,
  Modal,
  CardHeader
} from 'react-bootstrap';

const ConsultarFacturas = () => {

    const [loading, setLoading] = useState(false);
    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        setLoading(true);
    }
    
    return (
<Card>
    <CardHeader>Consultar Facturas </CardHeader>
    <Card.Body>
        <Form onSubmit={handleSubmit}>
            <FormGroup as={Row} className="mb-3" controlId="formRFC">
                <FormLabel column sm={2}>
                    RFC
                </FormLabel>
                <Col sm={10}>
                    <FormControl type="text" placeholder="Ingrese RFC" />
                </Col>
                <Button disabled={loading} variant="primary" type="submit" className="mt-3">
                    Consultar
                </Button>
                {loading ? (
                                  <>
                                    <Spinner animation="border" size="sm" className="me-2" />
                                    Consultando...
                                  </>
                                ) : (
                                  'Consultar Facturas'
                                )}
            </FormGroup>
        </Form>
    </Card.Body>
</Card>

    )
};

export default ConsultarFacturas;