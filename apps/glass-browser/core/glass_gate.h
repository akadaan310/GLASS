#pragma once
/* GLASS Gate ABI v1: static contract for trusted packaged Android .so modules.
 * A matching DLL can be inspected as bytes, not executed as native Android code.
 * Plugins must be packaged, signed, allowlisted, and version-checked at install.
 */
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
#define GLASS_GATE_ABI 1u
typedef struct glass_gate_v1 {
  uint32_t abi_version;
  const char *id;
  const char *capabilities;
  /* Return 0 on success; no ambient filesystem/network API exposed here. */
  int (*invoke)(const uint8_t *input, size_t length,
                uint8_t *output, size_t capacity, size_t *written);
} glass_gate_v1;
/* Each approved module exports this symbol. */
typedef const glass_gate_v1 *(*glass_gate_entry_fn)(void);
#ifdef __cplusplus
}
#endif
