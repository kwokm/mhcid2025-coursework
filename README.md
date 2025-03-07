# MHCID 2025 Coursework

## Path Aliases

This project uses TypeScript path aliases to make imports more convenient. The following aliases are available:

- `@q1/*` - Points to files in the `q1fall` directory
- `@q2/*` - Points to files in the `q2winter` directory
- `@q3/*` - Points to files in the `q3spring` directory
- `@q4/*` - Points to files in the `q4summer` directory
- `@assets/*` - Points to files in the `assets` directory

### Example Usage

Instead of using relative paths like:

```typescript
import { Component } from '../../q1fall/components/Component';
import { image } from '../../../assets/images/image.png';
```

You can use the aliases:

```typescript
import { Component } from '@q1/components/Component';
import { image } from '@assets/images/image.png';
```

This makes your imports cleaner and more maintainable, especially when moving files around in the project structure.

### IDE Support

For the best experience, ensure your IDE supports TypeScript path aliases. Most modern IDEs like VS Code will automatically recognize the aliases defined in `tsconfig.json`.