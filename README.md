# Overview
Playground app modelling candidate simple path in a recruitment process implementing
Event Sourcing(ES) + Command Query Resposibility Segregation (CQRS) concepts.

Command path is represented by `Candidate` aggregate. The aggregate is build on
streams of sequential events, that are persisted (instead of persisting state itself).
Query path is represented by `CandidateProjection` read model and is build by
handling `Candidate` dispatched events.

### Read model synchronization options
- `LocalEventPublisher` that is a simplified implementation of event bus. There is no
  message broker, published events are directly passed to event handlers.
- any implementation of real event bus / message broker (RabbitMQ, Kafka).
  Thanks to it, read model can be placed in other module / application / system,
  and update is eventually consistent

### Solution architecture
Application Architecture is port and adapters.
- secondary ports (interfaces) in application and domain layers
- secondary adapters (implementations) in infrastructure layer
- primary ports (application service and handlers) in application layer
- primary adapter (API for incoming request) is not implemented

### Development
The implementation is simplified and omits some important aspects like:
- events versioning
- concurrency version control
- snapshoting of an aggregate
- genuine event bus implementation
- API to transport incoming requests

Huge part of this code was inspired by: https://breadcrumbscollector.tech/category/event-sourcing/

# Install packages
`>> pip install -r dev_requirements.txt`

# Run tests
`>> PYTHONPATH=src pytest -x`