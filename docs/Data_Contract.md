# Data Contract

## Current status
Week 1 initializes the repository and environment only.

## Planned content
This document will later describe:
- data source;
- schema and columns;
- refresh frequency;
- quality rules;
- storage layers (`raw`, `normalized`, `mart`).

## Current status
Week 2 implements a template version of the Extract layer.

The final semester-specific API configuration will be added after receiving the official `variant_XX.yml` file from the course materials.

## Planned source description
- Source type: `TBD`
- Theme: `TBD`

## API
- Base URL: `TBD`
- Method: `GET`
- Request template: `TBD`
- Parameters: `TBD`

## Load frequency
- Manual запуск during development
- Planned automation in later weeks

## Raw layer
Raw API responses are saved without transformations for reproducibility:

```text
data/raw/variant_XX/YYYY-MM-DD_HH-MM-SS.json
```

## Notes / limitations
- Timeout is required to prevent hanging requests.
- HTTP errors must be handled explicitly.
- JSON parsing must be protected from invalid responses.
- Final values will be filled in after receiving the official variant configuration.
