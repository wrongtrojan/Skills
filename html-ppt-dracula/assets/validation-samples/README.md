# Validation Negative Samples

These fixtures are intentionally invalid and are used to verify validator failure paths.

## Samples

- `placeholder-fail.html`: unresolved placeholder tokens (`[PLACEHOLDER]` style) should fail.
- `conflict-fail.html`: conflicting components enabled together should fail.
- `duplicate-key-fail.html`: duplicate enabled component keys should fail.
- `section-order-fail.html`: section order mismatch against component section mapping should fail.

## Example Commands

```bash
python scripts/validate_structure.py assets/validation-samples/placeholder-fail.html
python scripts/validate_structure.py assets/validation-samples/conflict-fail.html
python scripts/validate_structure.py assets/validation-samples/duplicate-key-fail.html
python scripts/validate_structure.py assets/validation-samples/section-order-fail.html
```
