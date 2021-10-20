# recruitment
Playground app modelling candidate simple path in a recruitment using Event Sourcing + CQRS

Command path is represented by `Candidate` aggregate.
Query path is represented by `CandidateProjection` read model.

Read model can be synchronized using:
- `LocalEventPublisher` that is a simplified implementation of event bus. There is no
  message broker, published events are directly passed to event handlers.
- any implementation of real event bus / message broker (RabbitMQ, Kafka).
  Thanks to it, read model can be placed in other module / application / system,
  and update is eventually consistent