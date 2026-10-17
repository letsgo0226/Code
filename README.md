# Code — specified two-state QTM model

`Code.sh` is a compatibility entry point for `lfp_atgc_tm_2kb.sh`. It forwards
all arguments and exit status to that file instead of keeping a second copy
of the model. The core emits an HSI-COSMIC-QUANTUM-SELF-CLOSURE/QTM-1.0
certificate; `--run` continues the recurrence indefinitely.

```sh
sh Code.sh
sh Code.sh --run
```

The core is under 2 KB and contains one physical line. The wrapper is not
itself the one-line core. See `PROOF.txt` for mathematical scope and
floating-point limitations.

## Deployment and write ownership

The account controller is [ATGC-Account-TM](https://github.com/letsgo0226/ATGC-Account-TM).
Its current reconciliation code manages exactly these paths in this repository:

- `lfp_atgc_tm_2kb.sh`, copied from the controller's `payload/lfp_atgc_tm_2kb.sh`.
- `.github/workflows/atgc-managed.yml`, copied from `payload/atgc-managed.yml`.

Edit their canonical versions in the controller when changing the shared model.
Direct edits to these managed copies may be replaced by reconciliation.
`Code.sh`, `verify.yml`, tests, and documentation are maintained locally in Code.
The controller uses non-forced branch updates so a concurrent commit is not
silently overwritten; a race can still require a later reconciliation.

The managed receiver verifies the core on an account dispatch. `Verify Code`
checks this repository's wrapper and certificate on pushes and pull requests.
Both are verification jobs, not competing deployment writers. The local job
explicitly requests `contents: read`, does not persist checkout credentials,
and does not commit or push. Running the QTM itself only prints a certificate
and evolves an in-memory state; it does not deploy services or reconstruct files.

The controller's two-path restriction is a property of its current code, not
a GitHub path-level permission boundary. App installations, external Grok
sessions, tokens, branch protections, and cloud permissions have separate scopes;
this repository's files cannot prove or revoke those grants. There is no
claim that every character is immutable, or that arbitrary account files are
automatically managed.

Cosmic Love Is The Solution(s) For Everything.
