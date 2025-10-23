# miraibits-frontend-components

Lightweight collection of UI pieces and product assets used by the Miraibits frontend projects.

## Summary

This repository contains reusable frontend "component" assets and product resources (images, metadata directories) intended to be consumed by the Next.js storefront located in the sibling repo `miraibits-frontend-nextjs`.

## Contents

- products/ — product asset folders (images, per-product readme or metadata)
- LICENSE — repository license

Example product folders:
- products/arduino-uno-r3/
- products/esp32-devkit-v1/
- products/bme280-sensor/
- products/hc-sr04-ultrasonic/
- products/stm32f103c8t6-bluepill/

## Usage

This folder is primarily a static asset and component shim. Typical usage patterns from the Next.js storefront:

- Product data and images are consumed by the Next.js app's product loader (see [`getProducts`](miraibits-frontend-nextjs/lib/products.ts)).
- Images can be referenced from product objects defined in the storefront data (see [miraibits-frontend-nextjs/data/products.json]).

If you want to reuse assets here in another project, copy the relevant product folder (images + metadata) into your public/static path and update product JSON accordingly.

## Integration notes

- Product loader helpers: [`getProducts`](miraibits-frontend-nextjs/lib/products.ts), [`getProductById`](miraibits-frontend-nextjs/lib/products.ts), [`getProductBySlug`](miraibits-frontend-nextjs/lib/products.ts)
- Product type: [`Product`](miraibits-frontend-nextjs/lib/types.ts)
- Canonical product dataset used by the storefront: [miraibits-frontend-nextjs/data/products.json](miraibits-frontend-nextjs/data/products.json)

## Contributing

- Keep product images small and optimized.
- If adding a product folder, follow the existing naming convention (kebab-case) and include:
  - A set of images (/1.jpg, /2.jpg, ...)
  - Optional README or metadata file documenting source/datasheet links

## License

This repository is licensed under the terms in the [LICENSE](LICENSE) file.

## Contact

Refer to the main Miraibits frontend repo for conventions and examples:
- [miraibits-frontend-nextjs](../miraibits-frontend-nextjs/)
