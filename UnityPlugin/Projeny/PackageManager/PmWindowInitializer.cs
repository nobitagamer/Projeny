using System;
using System.IO;
using UnityEditorInternal;
using UnityEngine;
using UnityEditor;
using System.Collections;
using System.Collections.Generic;
using Projeny.Internal;
using System.Linq;

namespace Projeny.Internal
{
    public class PmWindowInitializer
    {
        readonly PmReleasesHandler _releasesHandler;
        readonly PmPackageHandler _packageHandler;
        readonly PmProjectHandler _projectHandler;
        readonly AsyncProcessor _asyncProcessor;
        bool _isInitialized;

        public PmWindowInitializer(
            PmProjectHandler projectHandler,
            PmPackageHandler packageHandler,
            PmReleasesHandler releasesHandler,
            AsyncProcessor asyncProcessor)
        {
            _releasesHandler = releasesHandler;
            _packageHandler = packageHandler;
            _projectHandler = projectHandler;
            _asyncProcessor = asyncProcessor;
        }

        public bool IsInitialized
        {
            get
            {
                return _isInitialized;
            }
        }

        public void Initialize(bool isFirstLoad)
        {
            _asyncProcessor.Process(InitializeAsync(isFirstLoad), true, "Initializing Projeny");
        }

        IEnumerator InitializeAsync(bool isFirstLoad)
        {
            Assert.That(!_isInitialized);

            if (isFirstLoad)
            {
                _projectHandler.RefreshProject();

                yield return _packageHandler.RefreshPackagesAsync();
                yield return _releasesHandler.RefreshReleasesAsync();
            }

            _isInitialized = true;
        }
    }
}
